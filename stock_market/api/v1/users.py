from django.urls import path
from rest_framework.routers import DefaultRouter
from users.views import (
    TokenAPIView,
    TokenRefreshAPIView,
    UserChangePasswordViewSet,
    UserViewSet,
)

user_router = DefaultRouter()
user_router.register(r"users", UserViewSet)

password_router = DefaultRouter()
password_router.register(r"change-password", UserChangePasswordViewSet)

urlpatterns = [
    path("tokens/", TokenAPIView.as_view()),
    path("tokens/refresh", TokenRefreshAPIView.as_view()),
]

urlpatterns += user_router.urls
urlpatterns += password_router.urls
