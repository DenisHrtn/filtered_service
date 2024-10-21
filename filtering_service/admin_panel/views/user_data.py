from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from decouple import config
from django.db import transaction
from rest_framework import parsers

from admin_panel.models import UserData
from admin_panel.serializers.user_data_serializer import UserDataSerializer
from filtering_service.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema


PROXY_SECRET_KEY = config('PROXY_SECRET_KEY')


class UserDataView(GenericAPIView):
    serializer_class = UserDataSerializer
    parser_classes = (parsers.JSONParser, parsers.MultiPartParser)
    # proxy_secret_key = request.headers.get('X-Proxy-Auth')
    #
    # if proxy_secret_key != PROXY_SECRET_KEY or not proxy_secret_key:
    #     return Response({'error': 'Unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        #

        if not isinstance(request.data, list):
            return Response({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)

        object_list = []
        for item in request.data:
            serializer = UserDataSerializer(data=item)

            if serializer.is_valid(raise_exception=True):
                object_list.append(UserData(**serializer.validated_data))
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if object_list:
            with transaction.atomic():
                UserData.objects.bulk_create(object_list)

        return Response({'message': 'Data successfully saved'}, status=status.HTTP_201_CREATED)


UserDataView = apply_swagger_auto_schema(
    tags=['upload data'], excluded_methods=[]
)(UserDataView)
