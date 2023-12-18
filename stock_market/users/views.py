from rest_framework import generics, mixins
from rest_framework.response import Response
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

    def get_object(self):
        return User.objects.get(pk=self.request.data["id"])

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data)


class UserChangePasswordAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
