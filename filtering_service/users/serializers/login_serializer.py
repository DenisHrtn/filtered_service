from rest_framework import serializers
from django.contrib.auth.hashers import check_password

from users.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if not check_password(data['password'], user.password):
            raise serializers.ValidationError("Invalid credentials")

        data['user'] = user

        return data