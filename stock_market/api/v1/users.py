from django.urls import path
from rest_framework.routers import DefaultRouter
from users.views import TokenRefreshAPIView, UserViewSet

user_router = DefaultRouter()
user_router.register(r"users", UserViewSet)

urlpatterns = [
    path("token/refresh/", TokenRefreshAPIView.as_view()),
]

urlpatterns += user_router.urls
