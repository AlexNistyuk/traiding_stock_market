from rest_framework.routers import DefaultRouter
from users.views import UserChangePasswordViewSet, UserViewSet

user_router = DefaultRouter()
user_router.register(r"users", UserViewSet)

password_router = DefaultRouter()
password_router.register(r"change-password", UserChangePasswordViewSet)

urlpatterns = user_router.urls
urlpatterns += password_router.urls
