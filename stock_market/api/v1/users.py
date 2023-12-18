from django.urls import path
from users.views import UserChangePasswordAPIView, UserListCreateUpdateAPIView

urlpatterns = [
    path("users/", UserListCreateUpdateAPIView.as_view()),
    path("users/change-password/", UserChangePasswordAPIView.as_view()),
]
