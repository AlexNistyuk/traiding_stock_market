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
from rest_framework.response import Response


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

    #
    # def get_object(self):
    #     return Investment.objects.get(pk=self.request.data["id"])

    def put(self, request, *args, **kwargs):
        self.kwargs["pk"] = request.data["id"]

        return self.update(request, *args, **kwargs)
        # instance = self.get_object()
        # serializer = self.get_serializer(instance, data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        #
        # return Response(data=serializer.data)


class MarketOrderListCreateUpdateAPIView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
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

    def get_object(self):
        return MarketOrder.objects.get(pk=self.request.data["id"])

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data)


class LimitOrderListCreateUpdateAPIView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
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

    def get_object(self):
        return LimitOrder.objects.get(pk=self.request.data["id"])

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data)


class InvestmentPortfolioListCreateUpdateAPIView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
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

    def get_object(self):
        return InvestmentPortfolio.objects.get(pk=self.request.data["id"])

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data)


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

    def get_object(self):
        return Trade.objects.get(pk=self.request.data["id"])

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data)


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

    def get_object(self):
        return Recommendation.objects.get(pk=self.request.data["id"])

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data)
