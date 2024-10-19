from rest_framework import serializers

from users.models.user import User


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=8)
    password_confirm = serializers.CharField(required=True, min_length=8)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists!")

        if password != password_confirm:
            raise serializers.ValidationError("Password are mismatch!")

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user
