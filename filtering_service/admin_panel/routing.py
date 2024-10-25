from django.urls import re_path
from .consumers import SendUserDataConsumer

websocket_urlpatterns = [
    re_path(r'ws/send-user-data/$', SendUserDataConsumer.as_asgi())
]
