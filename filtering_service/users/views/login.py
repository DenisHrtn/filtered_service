from rest_framework import permissions
from rest_framework import status
from rest_framework import parsers
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from filtering_service.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema
from users.serializers.login_serializer import LoginSerializer


class LoginView(GenericAPIView):
    permission_classes = [permissions.AllowAny, ]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, ]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        if user:
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            response = Response("Logged successfully", status=status.HTTP_200_OK)
            response.set_cookie(key='access_token', value=str(access_token), httponly=True, samesite='Lax')
            response.set_cookie(key='refresh_token', value=str(refresh_token), httponly=True, samesite='Lax')

            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


LoginView = apply_swagger_auto_schema(
    tags=['auth / register'], excluded_methods=[]
)(LoginView)