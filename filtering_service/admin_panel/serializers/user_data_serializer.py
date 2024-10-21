import re

from rest_framework import serializers
from admin_panel.models import UserData


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['email', 'endpoint', 'login', 'message', 'support_level', 'user_id', 'timestamp', 'phone_number',
                  'patronymic', 'birth_date', 'name', 'surname', 'age']

    def create(self, validated_data):
        print("Creating user data with:", validated_data)  # Для отладки

        # Проверка, не пустой ли validated_data
        if not validated_data:
            print("No data provided for creation")

        user_data = UserData(
            email=validated_data.get('Email'),
            endpoint=validated_data.get('Endpoint'),
            login=validated_data.get('Login'),
            message=validated_data.get('Message'),
            support_level=validated_data.get('SupportLevel'),
            user_id=validated_data.get('UserID'),
            timestamp=validated_data.get('Timestamp'),
            phone_number=validated_data.get('Номер телефона'),
            patronymic=validated_data.get('Отчество'),
            birth_date=validated_data.get('Дата рождения'),
            name=validated_data.get('Имя'),
            surname=validated_data.get('\ufeffФамилия'),  # Убедитесь, что вы используете правильный ключ
            age=validated_data.get('Возраст'),
        )

        user_data.save()
        return user_data