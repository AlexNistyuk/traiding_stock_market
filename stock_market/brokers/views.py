from brokers.models import (
    Investment,
    InvestmentPortfolio,
    LimitOrder,
    MarketOrder,
    Recommendation,
    Trade,
)
from brokers.permissions import IsBuyerOrSeller, IsOrderOwner
from brokers.serializers import (
    InvestmentCreateSerializer,
    InvestmentPortfolioCreateSerializer,
    InvestmentPortfolioRetrieveSerializer,
    InvestmentPortfolioUpdateSerializer,
    InvestmentRetrieveSerializer,
    InvestmentUpdateSerializer,
    LimitOrderCreateSerializer,
    LimitOrderRetrieveSerializer,
    LimitOrderUpdateSerializer,
    MarketOrderCreateSerializer,
    MarketOrderRetrieveSerializer,
    MarketOrderUpdateSerializer,
    RecommendationCreateSerializer,
    RecommendationRetrieveSerializer,
    RecommendationUpdateSerializer,
    TradeCreateSerializer,
    TradeRetrieveSerializer,
    TradeUpdateSerializer,
)
from django.http import Http404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.permissions import IsAdmin, IsAnalyst, IsOwner
from utils.services import (
    InvestmentPortfolioService,
    LimitOrderService,
    MarketOrderService,
    TradeService,
)


class InvestmentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Investment.objects.all()
    serializer_action_classes = {
        "list": InvestmentRetrieveSerializer,
        "retrieve": InvestmentRetrieveSerializer,
        "create": InvestmentCreateSerializer,
        "update": InvestmentUpdateSerializer,
        "partial_update": InvestmentUpdateSerializer,
    }
    permission_action_classes = {
        "create": [IsAdmin],
        "update": [IsAdmin],
        "partial_update": [IsAdmin],
    }

    @property
    def permission_classes(self):
        return self.permission_action_classes.get(self.action, [])

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]


class MarketOrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = MarketOrder.objects.all()
    serializer_action_classes = {
        "list": MarketOrderRetrieveSerializer,
        "retrieve": MarketOrderRetrieveSerializer,
        "create": MarketOrderCreateSerializer,
        "update": MarketOrderUpdateSerializer,
        "partial_update": MarketOrderUpdateSerializer,
    }
    permission_action_classes = {
        "list": [IsAdmin | IsAnalyst],
        "retrieve": [IsAdmin | IsAnalyst],
        "update": [IsAdmin],
        "partial_update": [IsAdmin],
    }

    def get_object(self):
        try:
            instance = MarketOrder.objects.select_related(
                "portfolio", "investment"
            ).get(pk=self.kwargs["pk"])
        except MarketOrder.DoesNotExist:
            raise Http404

        self.check_object_permissions(self.request, instance)

        return instance

    @property
    def permission_classes(self):
        return self.permission_action_classes.get(self.action, [])

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = MarketOrderService(serializer.validated_data).create()

        return Response(
            self.get_serializer(instance).data, status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.get_object()
        instance = MarketOrderService(
            serializer.validated_data, instance=instance
        ).update()

        return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)


class LimitOrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = LimitOrder.objects.all()
    serializer_action_classes = {
        "list": LimitOrderRetrieveSerializer,
        "retrieve": LimitOrderRetrieveSerializer,
        "create": LimitOrderCreateSerializer,
        "update": LimitOrderUpdateSerializer,
        "partial_update": LimitOrderUpdateSerializer,
    }
    permission_action_classes = {
        "list": [IsAdmin | IsAnalyst],
        "retrieve": [IsAdmin | IsAnalyst | IsOrderOwner],
        "update": [IsAdmin],
        "partial_update": [IsAdmin],
    }

    def get_object(self):
        try:
            instance = LimitOrder.objects.select_related("portfolio", "investment").get(
                pk=self.kwargs["pk"]
            )
        except LimitOrder.DoesNotExist:
            raise Http404

        self.check_object_permissions(self.request, instance)

        return instance

    @property
    def permission_classes(self):
        return self.permission_action_classes.get(self.action, [])

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = LimitOrderService(serializer.validated_data).create()

        return Response(
            self.get_serializer(instance).data, status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.get_object()
        instance = LimitOrderService(
            serializer.validated_data, instance=instance
        ).update()

        return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)


class InvestmentPortfolioViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = InvestmentPortfolio.objects.all()
    serializer_action_classes = {
        "list": InvestmentPortfolioRetrieveSerializer,
        "retrieve": InvestmentPortfolioRetrieveSerializer,
        "own": InvestmentPortfolioRetrieveSerializer,
        "create": InvestmentPortfolioCreateSerializer,
        "update": InvestmentPortfolioUpdateSerializer,
        "partial_update": InvestmentPortfolioUpdateSerializer,
    }
    permission_action_classes = {
        "list": [IsAdmin],
        "retrieve": [IsAdmin | IsOwner],
        "update": [IsAdmin],
        "partial_update": [IsAdmin],
    }

    @property
    def permission_classes(self):
        return self.permission_action_classes.get(self.action, [])

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    def get_object(self):
        try:
            instance = InvestmentPortfolio.objects.select_related(
                "owner", "investment"
            ).get(pk=self.kwargs["pk"])
        except InvestmentPortfolio.DoesNotExist:
            raise Http404

        self.check_object_permissions(self.request, instance)

        return instance

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = InvestmentPortfolioService(serializer.validated_data).create()

        return Response(
            self.get_serializer(instance).data, status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.get_object()
        instance = InvestmentPortfolioService(
            serializer.validated_data, instance=instance
        ).update()

        return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="own")
    def own(self, request, *args, **kwargs):
        queryset = InvestmentPortfolio.objects.filter(owner=request.jwt_user)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TradeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Trade.objects.all()
    serializer_action_classes = {
        "list": TradeRetrieveSerializer,
        "retrieve": TradeRetrieveSerializer,
        "create": TradeCreateSerializer,
        "update": TradeUpdateSerializer,
        "partial_update": TradeUpdateSerializer,
    }
    # TODO if not admin, return not all trades, only user's trades
    permission_action_classes = {
        "list": [IsAdmin | IsAnalyst],
        "retrieve": [IsAdmin | IsAnalyst | IsBuyerOrSeller],
        "update": [IsAdmin],
        "partial_update": [IsAdmin],
    }

    def get_object(self):
        try:
            instance = Trade.objects.select_related(
                "buyer", "seller", "investment"
            ).get(pk=self.kwargs["pk"])
        except Trade.DoesNotExist:
            raise Http404

        self.check_object_permissions(self.request, instance)

        return instance

    @property
    def permission_classes(self):
        return self.permission_action_classes.get(self.action, [])

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = TradeService(serializer.validated_data).create()

        return Response(
            self.get_serializer(instance).data, status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.get_object()
        instance = TradeService(serializer.validated_data, instance=instance).update()

        return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)


class RecommendationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Recommendation.objects.all()
    serializer_action_classes = {
        "list": RecommendationRetrieveSerializer,
        "retrieve": RecommendationRetrieveSerializer,
        "create": RecommendationCreateSerializer,
        "update": RecommendationUpdateSerializer,
        "partial_update": RecommendationUpdateSerializer,
    }
    # TODO if not admin, return not all recommendations, only user's trades
    permission_action_classes = {
        "list": [IsAdmin | IsAnalyst],
        "retrieve": [IsAdmin | IsAnalyst],
        "update": [IsAdmin],
        "partial_update": [IsAdmin],
    }

    @property
    def permission_classes(self):
        return self.permission_action_classes.get(self.action, [])

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]
