from django.contrib.auth import logout
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework import generics
from rest_framework.parsers import JSONParser, MultiPartParser

from filtering_service.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema


class EmptySerializer(serializers.Serializer):
    pass


class LogoutView(generics.GenericAPIView):
    serializer_class = EmptySerializer
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request):
        logout(request)
        response = HttpResponse(status=200)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response


LogoutView = apply_swagger_auto_schema(
    tags=['auth / register'], excluded_methods=[]
)(LogoutView)
