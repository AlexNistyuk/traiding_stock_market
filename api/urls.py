from django.urls import path, include

from .v1.users import urlpatterns as api_users
from .v1.brokers import urlpatterns as api_brokers

urlpatterns = [
    path("v1/", include(api_users)),
    path("api/", include(api_brokers)),
]