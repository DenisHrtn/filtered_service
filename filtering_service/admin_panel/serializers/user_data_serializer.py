from rest_framework import serializers
from admin_panel.models import UserData


class UserDataSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    name = serializers.CharField(required=False)
    surname = serializers.CharField(required=False)
    patronymic = serializers.CharField(required=False, allow_null=True)
    birth_date = serializers.DateField(required=False)
    gender = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False, allow_null=True)
    age = serializers.IntegerField(required=False)
    user_id = serializers.IntegerField(required=False)
    login = serializers.CharField(required=False)
    timestamp = serializers.IntegerField(required=False, allow_null=True)
    support_level = serializers.CharField(required=False)
    message = serializers.CharField(required=False)

    class Meta:
        model = UserData
        fields = [
            'email', 'name', 'surname', 'patronymic', 'birth_date',
            'gender', 'phone_number', 'age', 'user_id',
            'login', 'timestamp', 'support_level', 'message'
        ]
