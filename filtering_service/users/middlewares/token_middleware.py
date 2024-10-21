from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from datetime import datetime
from django.http import HttpResponse


User = get_user_model()


class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access_token = request.COOKIES.get('access_token')

        if access_token:
            try:
                AccessToken(access_token)
                response = self.get_response(request)
                return response

            except TokenError as e:
                print(e)
                try:
                    refresh_token = request.COOKIES.get('refresh_token')
                    refresh_token = RefreshToken(refresh_token)

                    exp_timestamp = refresh_token["exp"]
                    exp_datetime = datetime.utcfromtimestamp(exp_timestamp)
                    print("Время истечения refresh_token:", exp_datetime)

                    current_time = datetime.utcnow()
                    print("current time = ", datetime.utcfromtimestamp(current_time.timestamp()))
                    if exp_timestamp < current_time.timestamp():
                        raise TokenError("Refresh token has expired.")

                    user = User.objects.get(pk=refresh_token.payload.get('user_id'))
                    new_access_token = AccessToken.for_user(user)
                    response = HttpResponseRedirect(request.path_info)
                    print("middleware set new access_token")
                    response.set_cookie(key='access_token', value=str(new_access_token), httponly=True)
                    return response
                except TokenError as e:
                    print("refresh_token exception = ", e)

                    response = HttpResponse("refresh_token exception. Cookies Removed.")
                    response.delete_cookie('access_token')
                    response.delete_cookie('refresh_token')
                    return response

        response = self.get_response(request)
        return response
