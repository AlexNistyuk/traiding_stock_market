from brokers.models import Investment, LimitOrder
from django.contrib.postgres.aggregates import ArrayAgg
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User
from users.permissions import IsAdmin
from users.serializers import (
    ChangePasswordSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    UserRetrieveSerializer,
    UserSubscriptionSerializer,
    UserUpdateSerializer,
)
from utils.services import UserService
from utils.token import Token
from utils.trades import LimitOrderTrade


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
        "set_subscription": UserSubscriptionSerializer,
    }
    permission_action_classes = {
        "retrieve": [IsAdmin],
        "list": [IsAdmin],
        "update": [IsAdmin],
        "partial_update": [IsAdmin],
    }

    @property
    def permission_classes(self):
        return self.permission_action_classes.get(self.action, [])

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.get_object()
        instance = UserService(serializer.validated_data, instance=instance).update()

        return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = UserService(serializer.validated_data).create()

        return Response(
            self.get_serializer(instance).data, status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=["post"], url_path="change-password")
    def change_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        UserService(serializer.validated_data).change_password(request.jwt_user)

        return Response(
            data={"detail": "Successfully changed password"}, status=status.HTTP_200_OK
        )

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

    @action(detail=False, methods=["post"], url_path="subscription")
    def set_subscription(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        UserService(serializer.validated_data).set_subscriptions(request.jwt_user)

        return Response(
            data={"detail": "Successfully set subscriptions"}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["get"], url_path="test")
    def test(self, request, *args, **kwargs):
        result = (
            LimitOrder.objects.values("investment")
            .annotate(id=ArrayAgg("id"))
            .filter(status="active")
        )

        investments = Investment.objects.filter(
            id__in=[data["investment"] for data in result]
        )
        orders = LimitOrderTrade().get_orders(investment=investments[1])

        return orders


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
