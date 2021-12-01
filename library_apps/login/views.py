#General
import logging as log
import os, sys

#Django
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from library_apps.login.serializers import RegisterSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

#Utils
from library_apps.utils.status_http import StatusHttp

#Register API
class RegisterApi(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "message": "User Created Successfully.  Now perform Login to get your token",
            })

        except KeyError as error:
            return Response(**StatusHttp.status(status_type=400, \
                description_error=f"Key required: {str(error)}"))
        except Exception as error:
            log.error(error)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, "libro")
            return Response(**StatusHttp.status(status_type=500, description_error=str(error)))
