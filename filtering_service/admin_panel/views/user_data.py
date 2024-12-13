from rest_framework import viewsets, permissions

from admin_panel.models import UserData
from admin_panel.serializers.user_data_serializer import UserDataSerializer
from filtering_service.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema
from admin_panel.mixins import SaveUsersDataMixin


class UserDataView(SaveUsersDataMixin, viewsets.ModelViewSet):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer
    permission_classes = [permissions.AllowAny, ]


UserDataView = apply_swagger_auto_schema(
    tags=['upload data'], excluded_methods=[]
)(UserDataView)
