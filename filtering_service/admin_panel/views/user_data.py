from rest_framework import status, permissions, generics
from rest_framework.response import Response
from decouple import config
from django.db import transaction

from admin_panel.models import UserData
from admin_panel.serializers.user_data_serializer import UserDataSerializer
from filtering_service.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema


PROXY_SECRET_KEY = config('PROXY_SECRET_KEY')


class UserDataView(generics.CreateAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        proxy_secret_key = request.headers.get('X-Proxy-Auth')

        if proxy_secret_key != PROXY_SECRET_KEY or not proxy_secret_key:
            return Response({'error': 'Unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data

        print("Received data:", data)

        if isinstance(data, list):
            for item in data:
                serializer = self.get_serializer(data=item)
                serializer.is_valid(raise_exception=True)
                print(item)

                objects_list = []

                email = item.get('Email', None)
                endpoint = item.get('Endpoint', None)
                login = item.get('Login', None)
                message = item.get('Message', None)
                support_level = item.get('SupportLevel', None)
                timestamp = item.get('Timestamp', None)
                user_id = item.get('UserID', None)
                phone_number = item.get('Номер телефона', None)
                name = item.get('Имя', None)
                surname = item.get('Фамилия', None)
                patronymic = item.get('Отчество', None)
                gender = item.get('Пол', None)
                age = item.get('Возраст', None)
                birth_date = item.get('Дата рождения', None)

                objects_list.append(email)
                objects_list.append(endpoint)
                objects_list.append(login)
                objects_list.append(message)
                objects_list.append(support_level)
                objects_list.append(timestamp)
                objects_list.append(user_id)
                objects_list.append(phone_number)
                objects_list.append(name)
                objects_list.append(surname)
                objects_list.append(patronymic)
                objects_list.append(gender)
                objects_list.append(age)
                objects_list.append(birth_date)

                user_data = UserData(
                    email=email,
                    endpoint=endpoint,
                    login=login,
                    message=message,
                    support_level=support_level,
                    timestamp=timestamp,
                    user_id=user_id,
                    phone_number=phone_number,
                    name=name,
                    surname=surname,
                    patronymic=patronymic,
                    gender=gender,
                    age=age,
                    birth_date=birth_date,
                )

                with transaction.atomic():
                    user_data.save()
            return Response({'message': 'Данные успешно сохранены'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Неверный формат данных'}, status=status.HTTP_400_BAD_REQUEST)


UserDataView = apply_swagger_auto_schema(
    tags=['upload data'], excluded_methods=[]
)(UserDataView)
