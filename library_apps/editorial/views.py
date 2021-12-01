"""Category views."""

__author__ = 'kcastanedat'

#Django REST framework
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

#Models
from library_apps.editorial.models import Editorial

#Serializers
from library_apps.editorial.serializers import EditorialSerializer

#Utils
from library_apps.utils.status_http import StatusHttp

class EditorialView(APIView):
    """
    Editorial Book View.
    Allows you to list editorials of books stored in the db
    """

    def get(self, request):
        """
        Method that allows you to list editorials.
        """
        try:
            self.__request = request.query_params

            #In the url there is no parameter
            if len(self.__request) == 0:
                self.__queryset = Editorial.objects.all()
                self.__serializers = EditorialSerializer(self.__queryset, many=True)
                return Response(self.__serializers.data, **StatusHttp.status(200))

            #In the url comes the parameter id_editorial
            if self.__request.get('id_editorial'):
                self.__serializers = EditorialSerializer(Editorial.objects.filter(\
                    id_editorial=self.__request.get('id_editorial')), many=True)
                if len(self.__serializers.data) > 0:
                    return Response(self.__serializers.data, **StatusHttp.status(200))
                return Response(**StatusHttp.status(404))

            #In the url there is an invalid parameter
            return Response(**StatusHttp.status(400, description_error=\
                "Key required '{0}'".format('id_editorial')))

        except Exception as error:
            return Response(**StatusHttp.status(status_type=500, description_error=str(error)))

    def post(self, request):
        """
        Method for creating editorials.
        """
        try:
            self.__request = request.data
            editorial_book = EditorialSerializer(data=self.__request)

            #The case that the data is correct
            if editorial_book.is_valid():
                editorial_exist = Editorial.objects.filter(Q(id_editorial=\
                    self.__request.get('id_editorial')) | Q(editorial=\
                    self.__request.get('editorial'))).count()

                #The case in which the editorial to be created already exists
                if editorial_exist > 0:
                    return Response(**StatusHttp.status(status_type=400,\
                        description_error="The book editorial already exists."))

                #Save the editorial
                editorial_book.save()
                return Response(**StatusHttp.status(201))

            return Response(**StatusHttp.status(status_type=400, \
                description_error=f"Error: {str(editorial_book.errors)}"))
        except KeyError as error:
            return Response(**StatusHttp.status(status_type=400, \
                description_error=f"Key required: {str(error)}"))
        except Exception as error:
            return Response(**StatusHttp.status(status_type=500, description_error=str(error)))
