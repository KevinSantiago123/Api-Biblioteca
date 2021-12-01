"""Category views."""

__author__ = 'kcastanedat'

#Django REST framework
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

#Models
from library_apps.category.models import Category

#Serializers
from library_apps.category.serializers import CategorySerializer

#Utils
from library_apps.utils.status_http import StatusHttp

class CategoryView(APIView):
    """
    Category Book View.
    Allows you to list categories of books stored in the db
    """

    def get(self, request):
        """
        Method that allows you to list category of books.
        """
        try:
            self.__request = request.query_params

            #In the url there is no parameter
            if len(self.__request) == 0:
                self.__queryset = Category.objects.all()
                self.__serializers = CategorySerializer(self.__queryset, many=True)
                return Response(self.__serializers.data, **StatusHttp.status(200))

            #In the url comes the parameter id_categoria
            if self.__request.get('id_categoria'):
                self.__serializers = CategorySerializer(Category.objects.filter(\
                    id_categoria=self.__request.get('id_categoria')), many=True)
                if len(self.__serializers.data) > 0:
                    return Response(self.__serializers.data, **StatusHttp.status(200))
                return Response(**StatusHttp.status(404))

            #In the url there is an invalid parameter
            return Response(**StatusHttp.status(400, description_error=\
                "Key required '{0}'".format('id_categoria')))

        except Exception as error:
            return Response(**StatusHttp.status(status_type=500, description_error=str(error)))

    def post(self, request):
        """
        Method for creating category.
        """
        try:
            self.__request = request.data
            category_book = CategorySerializer(data=self.__request)

            #The case that the data is correct
            if category_book.is_valid():
                category_exist = Category.objects.filter(Q(id_categoria=\
                    self.__request.get('id_categoria')) | Q(categoria=\
                    self.__request.get('categoria'))).count()

                #The case in which the category to be created already exists
                if category_exist > 0:
                    return Response(**StatusHttp.status(status_type=400,\
                        description_error="The book category already exists."))

                #Save the category
                category_book.save()
                return Response(**StatusHttp.status(201))

            return Response(**StatusHttp.status(status_type=400, \
                description_error=f"Error: {str(category_book.errors)}"))
        except KeyError as error:
            return Response(**StatusHttp.status(status_type=400, \
                description_error=f"Key required: {str(error)}"))
        except Exception as error:
            return Response(**StatusHttp.status(status_type=500, description_error=str(error)))
