from django.urls import path
from rest_framework.routers import DefaultRouter
from users.views import TokenAPIView, TokenRefreshAPIView, UserViewSet

user_router = DefaultRouter()
user_router.register(r"users", UserViewSet)

urlpatterns = [
    path("tokens/", TokenAPIView.as_view()),
    path("tokens/refresh", TokenRefreshAPIView.as_view()),
]

urlpatterns += user_router.urls
