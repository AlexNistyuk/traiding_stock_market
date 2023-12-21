from django.urls import include, path

from .v1.brokers import urlpatterns as api_brokers
from .v1.users import urlpatterns as api_users

urlpatterns = [
    path("v1/", include(api_users + api_brokers)),
]
