"""Actividad views."""

__author__ = 'kcastanedat'

#General
import logging as log
import os, sys
import requests, json




#Django REST framework
from rest_framework.response import Response
from rest_framework.views import APIView

#Apis
from library_config.settings.base import URL_GOOGLE_BOOKS

#Models
from library_apps.book.models import Book, LibroAutor, LibroCategory
from library_apps.author.models import Author
from library_apps.editorial.models import Editorial
from library_apps.category.models import Category

#Serializers
from library_apps.book.serializers import (BookSerializer, GoogleSerializer,
    LibroAuthorSerializer, BookResponseSerializer, LibroCategorySerializer)
from library_apps.author.serializers import AuthorSerializer
from library_apps.editorial.serializers import EditorialSerializer
from library_apps.category.serializers import CategorySerializer

#Utils
from library_apps.utils.status_http import StatusHttp

def search_db_books(query, filter=False):
    """Allow the search of data in db with filter optional"""

    result = []
    exist_data = False

    #if filter is false the search by parameter
    if filter:
        queryset = Book.objects.filter(**query).values(
            'id_libro','titulo','subtitulo', 'fecha_publicacion', 'descripcion',
            'id_editorial__editorial')

    #if filter is true all the books are brought
    else:
        queryset = Book.objects.all().values()

    #get all values of id_libro
    books = [data['id_libro'] for data in queryset]

    #Search in the db his author, category
    queryset2 = LibroAutor.objects.filter(id_libro__in=books).values('id_libro',
        'id_autor__nombre')
    queryset3 = LibroCategory.objects.filter(id_libro__in=books).values('id_libro',
        'id_categoria__categoria')

    #Build the response
    if len(queryset) > 0:

        #Structure books
        for book in queryset:
            book['author'] = []
            book['category'] = []
            book['editorial'] = book.pop('id_editorial__editorial')
            for author in queryset2:
                if author['id_libro'] == book['id_libro']:
                    book['author'].append(author['id_autor__nombre'])
            for category in queryset3:
                if category['id_libro'] == book['id_libro']:
                    book['category'].append(category['id_categoria__categoria'])
        result.append({
            'source': 'db interna',
            'totalBooks': len(books),
            'books':queryset
        })
        exist_data = True
    return result, exist_data

def search_gooogle_books(param):
    """Allow the search of data in the API Google Books"""
    request = requests.get(URL_GOOGLE_BOOKS.format(param))
    if request.status_code == 200:
        result = request.json()
        result['source'] = 'Google Books'
        status = request.status_code
    return status, result

class BookView(APIView):
    """
    Book View.
    Permite listar libros almacenados en la db
    """
    def __init__(self):
        self.query = {}

    def get(self, request):
        """
        Allows you to list books.
        """
        try:
            self.__request = request.query_params
            #The data type of the parameters is validated
            request_book = BookSerializer(data=self.__request)

            if request_book.is_valid(raise_exception=True):
                if len(request_book.data) > 0:
                    #List dictionary to search by field type
                    key = [data for data in request_book.data.keys()]
                    value = [data for data in request_book.data.values()]
                    if isinstance(value[0], str):
                        self.query = {f"{key[0]}__contains": value[0]}
                    if isinstance(value[0], int):
                        self.query = request_book.data

                    #Search in the db the books by filter
                    result, exist_data = search_db_books(self.query, filter=True)

                    if exist_data:
                        return Response(result, **StatusHttp.status(200))

                    #In the case that the book does not exist in the db
                    status, result = search_gooogle_books(value[0])
                    if status == 200:
                        return Response(result, **StatusHttp.status(200))
                    return Response(**StatusHttp.status(status))

                return Response(**StatusHttp.status(400))
            return Response(**StatusHttp.status(status_type=400, \
                description_error=f"Error: {str(request_book.errors)}"))
        except IndexError as error:
            return Response(**StatusHttp.status(status_type=404))
        except Exception as error:
            log.error(error)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, "libro")
            return Response(**StatusHttp.status(status_type=500, description_error=str(error)))

    def post(self, request):
        """
        Method for creating Books.
        """
        try:
            self.__request = request.data
            google_book = GoogleSerializer(data=self.__request)

            #The case that the data is correct
            if google_book.is_valid():

                #get books in API Google Books
                status, result = search_gooogle_books(google_book.data.get('id'))
                if status == 200:
                    data = {
                        'id_autor':[],
                        'id_editorial':0,
                        'id_categoria':[],
                        'id_libro':0
                    }

                    #Validate Exist Books
                    try:
                        book = BookResponseSerializer(Book.objects.get(titulo=
                            result.get('items')[0].get('volumeInfo').get('title')))
                        return Response(**StatusHttp.status(status_type=400,\
                            description_error="The book already exists."))
                    except Book.DoesNotExist:
                        #Create Author
                        author_google = result.get('items')[0].get('volumeInfo').get('authors')
                        for author_go in author_google:
                            try:
                                author = AuthorSerializer(Author.objects.get(nombre=author_go))
                                data.get('id_autor').append(author.data.get('id_autor'))
                            except Author.DoesNotExist:
                                author = Author(nombre=author_go)
                                author.save()
                                author = AuthorSerializer(author)
                                data.get('id_autor').append(author.data.get('id_autor'))

                        #Create Editorial
                        editorial_google = result.get('items')[0].get('volumeInfo').get('printType')
                        try:
                            editorial = EditorialSerializer(Editorial.objects.get(editorial=editorial_google))
                            data['id_editorial'] = editorial.data.get('id_editorial')
                        except Editorial.DoesNotExist:
                            editorial = Editorial(editorial=editorial_google)
                            editorial.save()
                            editorial = EditorialSerializer(editorial)
                            data['id_editorial'] = editorial.data.get('id_editorial')

                        #Create Category
                        category_google = result.get('items')[0].get('volumeInfo').get('categories')
                        for category_go in category_google:
                            try:
                                category = CategorySerializer(Category.objects.get(categoria=category_go))
                                data.get('id_categoria').append(category.data.get('id_categoria'))
                            except Category.DoesNotExist:
                                category = Category(categoria=category_go)
                                category.save()
                                category = CategorySerializer(category)
                                data.get('id_categoria').append(category.data.get('id_categoria'))

                        #Create Books
                        self.query['titulo'] = result.get('items')[0].get('volumeInfo').get('title')
                        self.query['subtitulo'] = result.get('items')[0].get('volumeInfo').get('title')
                        self.query['fecha_publicacion'] = result.get('items')[0].get('volumeInfo').get('publishedDate')
                        self.query['descripcion'] = result.get('items')[0].get('volumeInfo').get('description')
                        self.query['id_editorial_id'] = data.get('id_editorial')
                        self.query['titulo'] = '' if self.query.get('titulo') is None else self.query.get('titulo')
                        self.query['subtitulo'] = '' if self.query.get('subtitulo') is None else self.query.get('subtitulo')
                        self.query['fecha_publicacion'] = '' if self.query.get('fecha_publicacion') is None else self.query.get('fecha_publicacion')
                        self.query['descripcion'] = '' if self.query.get('descripcion') is None else self.query.get('descripcion')

                        try:
                            book = BookResponseSerializer(Book.objects.get(titulo=self.query.get('titulo')))
                            data['id_libro'] = book.data.get('id_libro')
                        except Book.DoesNotExist:
                            book = Book(**self.query)
                            book.save()
                            book = BookResponseSerializer(book)
                            data['id_libro'] = book.data.get('id_libro')

                        #Crear LibroAutor
                        for id in data.get('id_autor'):
                            try:
                                libro_autor = LibroAuthorSerializer(LibroAutor.objects.get(id_libro_id=data.get('id_libro'), id_autor_id=id))
                            except LibroAutor.DoesNotExist:
                                libro_autor = LibroAutor(id_libro_id=data.get('id_libro'), id_autor_id=id)
                                libro_autor.save()
                                libro_autor = LibroAuthorSerializer(libro_autor)

                        #Crear LibroCategory
                        for id in data.get('id_categoria'):
                            try:
                                libro_categoria = LibroCategorySerializer(LibroCategory.objects.get(id_libro_id=data.get('id_libro'), id_categoria_id=id))
                            except LibroCategory.DoesNotExist:
                                libro_categoria = LibroCategory(id_libro_id=data.get('id_libro'), id_categoria_id=id)
                                libro_categoria.save()
                                libro_categoria = LibroCategorySerializer(libro_categoria)
                        return Response(**StatusHttp.status(201))
                return Response(**StatusHttp.status(status))
            return Response(**StatusHttp.status(status_type=400, \
                description_error=f"Error: {str(google_book.errors)}"))
        except KeyError as error:
            return Response(**StatusHttp.status(status_type=400, \
                description_error=f"Key required: {str(error)}"))
        except Exception as error:
            return Response(**StatusHttp.status(status_type=500, description_error=str(error)))

    def delete(self, request):
        self.__request = request.query_params
        try:
            libro_categoria = LibroCategory.objects.filter(id_libro_id=self.__request.get('id_libro')).delete()
            libro_autor = LibroAutor.objects.filter(id_libro_id=self.__request.get('id_libro')).delete()
            book = Book.objects.get(id_libro=self.__request.get('id_libro')).delete()
            return Response(**StatusHttp.status(status_type=204))
        except Book.DoesNotExist:
            return Response(**StatusHttp.status(status_type=404))
        except KeyError as error:
            return Response(**StatusHttp.status(status_type=400, \
                description_error=f"Key required: {str(error)}"))
        except Exception as error:
            return Response(**StatusHttp.status(status_type=500, description_error=str(error)))


