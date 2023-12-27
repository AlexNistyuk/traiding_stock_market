from brokers.models import (
    Investment,
    InvestmentPortfolio,
    LimitOrder,
    MarketOrder,
    Recommendation,
    Trade,
)
from brokers.permissions import IsPortfolioOwner
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
from brokers.utils import (
    InvestmentPortfolioService,
    LimitOrderService,
    MarketOrderService,
    TradeMaker,
    TradeService,
)
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.models import Roles
from users.permissions import IsAdmin, IsAnalyst, IsOwner


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
        "create": (IsAdmin,),
        "update": (IsAdmin,),
        "partial_update": (IsAdmin,),
    }

    @property
    def permission_classes(self):
        return self.permission_action_classes.get(self.action, (AllowAny,))

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
        "list": (IsAdmin | IsAnalyst,),
        "retrieve": (IsAdmin | IsAnalyst,),
        "update": (IsAdmin,),
        "partial_update": (IsAdmin,),
    }

    @property
    def permission_classes(self):
        return self.permission_action_classes.get(self.action, (AllowAny,))

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = MarketOrderService(serializer.validated_data).create()
        instance = TradeMaker().make_market_order(instance)

        data = self.get_serializer(instance).data

        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = MarketOrderService().get_by_id_or_404(self.kwargs["pk"])
        self.check_object_permissions(self.request, instance)

        instance = MarketOrderService(
            serializer.validated_data, instance=instance
        ).update()
        instance = TradeMaker().make_market_order(instance)

        data = self.get_serializer(instance).data

        return Response(data, status=status.HTTP_200_OK)


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
        "list": (IsAdmin | IsAnalyst,),
        "retrieve": (IsAdmin | IsAnalyst | IsPortfolioOwner,),
        "update": (IsAdmin,),
        "partial_update": (IsAdmin,),
    }

    @property
    def permission_classes(self):
        return self.permission_action_classes.get(self.action, (AllowAny,))

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = LimitOrderService(serializer.validated_data).create()
        instance = TradeMaker().make_limit_order(instance)

        data = self.get_serializer(instance).data

        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = LimitOrderService().get_by_id_or_404(self.kwargs["pk"])
        self.check_object_permissions(self.request, instance)

        instance = LimitOrderService(
            serializer.validated_data, instance=instance
        ).update()
        instance = TradeMaker().make_limit_order(instance)

        data = self.get_serializer(instance).data

        return Response(data, status=status.HTTP_200_OK)


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
        "list": (IsAdmin,),
        "retrieve": (IsAdmin | IsOwner,),
        "update": (IsAdmin,),
        "partial_update": (IsAdmin,),
    }

    @property
    def permission_classes(self):
        return self.permission_action_classes.get(self.action, (AllowAny,))

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = InvestmentPortfolioService(serializer.validated_data).create()

        data = self.get_serializer(instance).data

        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = InvestmentPortfolioService().get_by_id_or_404(self.kwargs["pk"])
        self.check_object_permissions(self.request, instance)

        instance = InvestmentPortfolioService(
            serializer.validated_data, instance=instance
        ).update()

        data = self.get_serializer(instance).data

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="own")
    def own(self, request, *args, **kwargs):
        portfolios = InvestmentPortfolioService().get_by_filters(owner=request.jwt_user)
        serializer = self.get_serializer(portfolios, many=True)

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
    permission_action_classes = {
        "retrieve": (IsAdmin | IsAnalyst | IsPortfolioOwner,),
        "update": (IsAdmin,),
        "partial_update": (IsAdmin,),
    }

    def get_queryset(self):
        if self.request.jwt_user.role in (Roles.ADMIN, Roles.ANALYST):
            return TradeService().get_all()

        portfolios = InvestmentPortfolioService().get_by_filters(
            owner=self.request.jwt_user
        )

        return TradeService().get_by_filters(portfolio__in=portfolios)

    @property
    def permission_classes(self):
        return self.permission_action_classes.get(self.action, (AllowAny,))

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = TradeService(serializer.validated_data).create()

        data = self.get_serializer(instance).data

        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = TradeService().get_by_id_or_404(self.kwargs["pk"])
        self.check_object_permissions(self.request, instance)

        instance = TradeService(serializer.validated_data, instance=instance).update()

        data = self.get_serializer(instance).data

        return Response(data, status=status.HTTP_200_OK)


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
    # TODO if not admin, return not all recommendations, only user's recommendations
    permission_action_classes = {
        "list": (IsAdmin | IsAnalyst,),
        "retrieve": (IsAdmin | IsAnalyst,),
        "update": (IsAdmin,),
        "partial_update": (IsAdmin,),
    }

    @property
    def permission_classes(self):
        return self.permission_action_classes.get(self.action, (AllowAny,))

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]
