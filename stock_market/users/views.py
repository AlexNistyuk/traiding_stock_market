from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User
from users.serializers import (
    ChangePasswordSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    UserRetrieveSerializer,
    UserUpdateSerializer,
)
from utils.token import Token


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_action_classes = {
        "retrieve": UserRetrieveSerializer,
        "list": UserRetrieveSerializer,
        "update": UserUpdateSerializer,
        "partial_update": UserUpdateSerializer,
        "change_password": ChangePasswordSerializer,
        "register": UserCreateSerializer,
        "login": UserLoginSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="change-password")
    def change_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        incorrect_response = Response(
            data={"detail": "Incorrect username or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return incorrect_response

        if not user.check_password(password):
            return incorrect_response

        token = Token(user)

        return Response(data=token.get_tokens(), status=status.HTTP_200_OK)


class TokenRefreshAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response(
                data={"detail": "Refresh token is missed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payload = Token.get_payload(refresh_token)
        if not payload or payload["type"] != "refresh_token":
            return Response(
                data={"detail": "Token is invalid"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(id=payload["id"])
        except User.DoesNotExist:
            return Response(
                data={"detail": "Token is invalid"}, status=status.HTTP_400_BAD_REQUEST
            )

        token = Token(user)

        return Response(data=token.get_tokens())
