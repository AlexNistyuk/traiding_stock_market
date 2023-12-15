from django.urls import path
from users.views import (
    UserChangePasswordAPIView,
    UserCreateAPIView,
    UserRetrieveUpdateAPIView,
)

urlpatterns = [
    path("users/", UserCreateAPIView.as_view()),
    path("users/<int:pk>/", UserRetrieveUpdateAPIView.as_view()),
    path("users/change-password/", UserChangePasswordAPIView.as_view()),
]
