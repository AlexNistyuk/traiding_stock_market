from brokers.models import (
    Investment,
    InvestmentPortfolio,
    LimitOrder,
    MarketOrder,
    Recommendation,
    Trade,
)
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
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from utils.managers import InvestmentPortfolioManager


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

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]


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

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]


class InvestmentPortfolioViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_action_classes = {
        "list": InvestmentPortfolioRetrieveSerializer,
        "retrieve": InvestmentPortfolioRetrieveSerializer,
        "create": InvestmentPortfolioCreateSerializer,
        "update": InvestmentPortfolioUpdateSerializer,
        "partial_update": InvestmentPortfolioUpdateSerializer,
    }
    queryset = InvestmentPortfolio.objects.all()

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = InvestmentPortfolioManager(serializer.validated_data).create()

        return Response(
            self.get_serializer(instance).data, status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)

        instance = InvestmentPortfolioManager(serializer.validated_data).update(
            serializer.instance
        )

        return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)


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

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]


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

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]
