from django.urls import path

from .views.user_data import UserDataView

urlpatterns = [
    path("upload-user-data/", UserDataView.as_view(), name="user_data"),
]
