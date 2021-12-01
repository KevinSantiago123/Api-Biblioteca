"""Author views."""

__author__ = 'kcastanedat'

#Django REST framework
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

#Models
from library_apps.author.models import Author

#Serializers
from library_apps.author.serializers import AuthorSerializer

#Utils
from library_apps.utils.status_http import StatusHttp

class AuthorView(APIView):
    """
    Author Book View.
    Allows you to list authors of books stored in the db
    """

    def get(self, request):
        """
        Method that allows you to list authors of books.
        """
        try:
            self.__request = request.query_params

            #In the url there is no parameter
            if len(self.__request) == 0:
                self.__queryset = Author.objects.all()
                self.__serializers = AuthorSerializer(self.__queryset, many=True)
                return Response(self.__serializers.data, **StatusHttp.status(200))

            #In the url comes the parameter id_author
            if self.__request.get('id_autor'):
                self.__serializers = AuthorSerializer(Author.objects.filter(
                    id_autor=self.__request.get('id_autor')), many=True)
                if len(self.__serializers.data) > 0:
                    return Response(self.__serializers.data, **StatusHttp.status(200))
                return Response(**StatusHttp.status(404))

            #In the url there is an invalid parameter
            return Response(**StatusHttp.status(400, description_error=
                "Key required '{0}'".format('id_autor')))

        except Exception as error:
            return Response(**StatusHttp.status(status_type=500, description_error=str(error)))

    def post(self, request):
        """
        Method for creating author.
        """
        try:
            self.__request = request.data
            author_book = AuthorSerializer(data=self.__request)

            #The case that the data is correct
            if author_book.is_valid():
                author_exist = Author.objects.filter(Q(id_autor=\
                    self.__request.get('id_autor')) | Q(nombre=\
                    self.__request.get('nombre'))).count()

                #The case in which the author to be created already exists
                if author_exist > 0:
                    print(author_exist)
                    return Response(**StatusHttp.status(status_type=400,\
                        description_error="The book author already exists."))

                #Save the author
                author_book.save()
                return Response(**StatusHttp.status(201))

            return Response(**StatusHttp.status(status_type=400, \
                description_error=f"Error: {str(author_book.errors)}"))
        except KeyError as error:
            return Response(**StatusHttp.status(status_type=400, \
                description_error=f"Key required: {str(error)}"))
        except Exception as error:
            return Response(**StatusHttp.status(status_type=500, description_error=str(error)))
