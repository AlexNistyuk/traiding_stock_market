from rest_framework import generics, mixins
from users.models import User
from users.serializers import (
    ChangePasswordSerializer,
    UserCreateSerializer,
    UserRetrieveSerializer,
    UserUpdateSerializer,
)


class UserCreateAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserRetrieveUpdateAPIView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView
):
    serializer_method_classes = {
        "get": UserRetrieveSerializer,
        "put": UserUpdateSerializer,
    }
    queryset = User.objects.all()

    def get_serializer_class(self):
        return self.serializer_method_classes[self.request.method.lower()]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class UserChangePasswordAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
