from rest_framework import generics, mixins, viewsets
from rest_framework.response import Response
from users.models import User
from users.serializers import (
    ChangePasswordSerializer,
    UserCreateSerializer,
    UserRetrieveSerializer,
    UserUpdateSerializer,
)
from utils.token import Token


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


class TokenAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                data={"detail": "Incorrect username or password"}, status=401
            )

        if not user.check_password(password):
            return Response(
                data={"detail": "Incorrect username or password"}, status=401
            )

        token = Token(user)

        return Response(data=token.get_tokens())


class TokenRefreshAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response(data={"detail": "Refresh token is missed"}, status=400)

        payload = Token().get_payload(refresh_token)
        if not payload:
            return Response(data={"detail": "Token is invalid"}, status=400)

        try:
            user = User.objects.get(id=payload["id"])
        except User.DoesNotExist:
            return Response(data={"detail": "User does not exist"}, status=404)

        token = Token(user)

        return Response(data=token.get_tokens())
