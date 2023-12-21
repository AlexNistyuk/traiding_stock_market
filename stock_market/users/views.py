from rest_framework import mixins, viewsets
from users.models import User
from users.serializers import (
    ChangePasswordSerializer,
    UserCreateSerializer,
    UserRetrieveSerializer,
    UserUpdateSerializer,
)


class UserViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_action_classes = {
        "retrieve": UserRetrieveSerializer,
        "list": UserRetrieveSerializer,
        "create": UserCreateSerializer,
        "update": UserUpdateSerializer,
        "partial_update": UserUpdateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]


# TODO: create action for this and include it to UserViewSet
class UserChangePasswordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
