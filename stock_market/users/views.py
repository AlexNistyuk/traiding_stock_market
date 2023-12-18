from rest_framework import generics, mixins
from users.models import User
from users.serializers import (
    ChangePasswordSerializer,
    UserCreateSerializer,
    UserRetrieveSerializer,
    UserUpdateSerializer,
)


class UserListCreateUpdateAPIView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    queryset = User.objects.all()
    serializer_method_classes = {
        "get": UserRetrieveSerializer,
        "post": UserCreateSerializer,
        "put": UserUpdateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_method_classes[self.request.method.lower()]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.kwargs[self.lookup_field] = request.data["id"]

        return self.update(request, *args, **kwargs)


class UserChangePasswordAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
