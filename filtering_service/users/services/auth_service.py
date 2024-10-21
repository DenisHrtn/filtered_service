from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError


User = get_user_model()


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get("access_token")

        if not access_token:
            return None
        try:
            access_token = AccessToken(access_token)
            user = User.objects.get(pk=access_token.payload.get('user_id'))
            return user, access_token
        except TokenError as e:
            print(e)
            return None