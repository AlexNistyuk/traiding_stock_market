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
from django.db.models import Q
from rest_framework import generics, mixins


class InvestmentListCreateUpdateAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    queryset = Investment.objects.all()
    serializer_method_classes = {
        "get": InvestmentRetrieveSerializer,
        "post": InvestmentCreateSerializer,
        "patch": InvestmentUpdateSerializer,
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


class MarketOrderListCreateUpdateAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    queryset = MarketOrder.objects.all()
    serializer_method_classes = {
        "get": MarketOrderRetrieveSerializer,
        "post": MarketOrderCreateSerializer,
        "put": MarketOrderUpdateSerializer,
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


class LimitOrderListCreateUpdateAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    queryset = LimitOrder.objects.all()
    serializer_method_classes = {
        "get": LimitOrderRetrieveSerializer,
        "post": LimitOrderCreateSerializer,
        "put": LimitOrderUpdateSerializer,
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


class InvestmentPortfolioListCreateUpdateAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    serializer_method_classes = {
        "get": InvestmentPortfolioRetrieveSerializer,
        "post": InvestmentPortfolioCreateSerializer,
        "put": InvestmentPortfolioUpdateSerializer,
    }
    queryset = LimitOrder.objects.all()

    def get_serializer_class(self):
        return self.serializer_method_classes[self.request.method.lower()]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.kwargs[self.lookup_field] = request.data["id"]

        return self.update(request, *args, **kwargs)


class InvestmentPortfolioTradeRetrieveAPIView(
    mixins.ListModelMixin, generics.GenericAPIView
):
    serializer_class = TradeRetrieveSerializer

    def get_queryset(self):
        portfolio = InvestmentPortfolio.objects.get(pk=self.kwargs["pk"])

        return Trade.objects.filter(Q(seller=portfolio) | Q(buyer=portfolio))

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TradeListCreateUpdateAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    queryset = Trade.objects.all()
    serializer_method_classes = {
        "get": TradeRetrieveSerializer,
        "post": TradeCreateSerializer,
        "put": TradeUpdateSerializer,
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


class RecommendationListCreateUpdateAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    queryset = Recommendation.objects.all()
    serializer_method_classes = {
        "get": RecommendationRetrieveSerializer,
        "post": RecommendationCreateSerializer,
        "put": RecommendationUpdateSerializer,
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
