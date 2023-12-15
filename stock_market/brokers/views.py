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


class InvestmentListCreateAPIView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Investment.objects.all()
    serializer_method_classes = {
        "get": InvestmentRetrieveSerializer,
        "post": InvestmentCreateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_method_classes[self.request.method.lower()]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class InvestmentRetrieveUpdateAPIView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView
):
    queryset = Investment.objects.all()
    serializer_method_classes = {
        "get": InvestmentRetrieveSerializer,
        "put": InvestmentUpdateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_method_classes[self.request.method.lower()]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class MarketOrderListCreateAPIView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = MarketOrder.objects.all()
    serializer_method_classes = {
        "get": MarketOrderRetrieveSerializer,
        "post": MarketOrderCreateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_method_classes[self.request.method.lower()]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MarketOrderRetrieveUpdateAPIView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView
):
    serializer_method_classes = {
        "get": MarketOrderRetrieveSerializer,
        "put": MarketOrderUpdateSerializer,
    }
    queryset = MarketOrder.objects.all()

    def get_serializer_class(self):
        return self.serializer_method_classes[self.request.method.lower()]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class LimitOrderListCreateAPIView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = LimitOrder.objects.all()
    serializer_method_classes = {
        "get": LimitOrderRetrieveSerializer,
        "post": LimitOrderCreateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_method_classes[self.request.method.lower()]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LimitOrderRetrieveUpdateAPIView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView
):
    serializer_method_classes = {
        "get": LimitOrderRetrieveSerializer,
        "put": LimitOrderUpdateSerializer,
    }
    queryset = LimitOrder.objects.all()

    def get_serializer_class(self):
        return self.serializer_method_classes[self.request.method.lower()]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class InvestmentPortfolioCreateAPIView(
    mixins.CreateModelMixin, generics.GenericAPIView
):
    serializer_class = InvestmentPortfolioCreateSerializer
    queryset = LimitOrder.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class InvestmentPortfolioRetrieveUpdateAPIView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView
):
    serializer_method_classes = {
        "get": InvestmentPortfolioRetrieveSerializer,
        "put": InvestmentPortfolioUpdateSerializer,
    }
    queryset = InvestmentPortfolio.objects.all()

    def get_serializer_class(self):
        return self.serializer_method_classes[self.request.method.lower()]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
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


class TradeListCreateAPIView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Trade.objects.all()
    serializer_method_classes = {
        "get": TradeRetrieveSerializer,
        "post": TradeCreateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_method_classes[self.request.method.lower()]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TradeRetrieveUpdateAPIView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView
):
    serializer_method_classes = {
        "get": TradeRetrieveSerializer,
        "put": TradeUpdateSerializer,
    }
    queryset = Trade.objects.all()

    def get_serializer_class(self):
        return self.serializer_method_classes[self.request.method.lower()]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class RecommendationListCreateAPIView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Recommendation.objects.all()
    serializer_method_classes = {
        "get": RecommendationRetrieveSerializer,
        "post": RecommendationCreateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_method_classes[self.request.method.lower()]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RecommendationRetrieveUpdateAPIView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView
):
    serializer_method_classes = {
        "get": RecommendationRetrieveSerializer,
        "put": RecommendationUpdateSerializer,
    }
    queryset = Recommendation.objects.all()

    def get_serializer_class(self):
        return self.serializer_method_classes[self.request.method.lower()]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
