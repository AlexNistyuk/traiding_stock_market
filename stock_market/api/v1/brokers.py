from brokers.views import (
    InvestmentListCreateUpdateAPIView,
    InvestmentPortfolioListCreateUpdateAPIView,
    InvestmentPortfolioTradeRetrieveAPIView,
    LimitOrderListCreateUpdateAPIView,
    MarketOrderListCreateUpdateAPIView,
    RecommendationListCreateUpdateAPIView,
    TradeListCreateUpdateAPIView,
)
from django.urls import path

urlpatterns = [
    path("investments/", InvestmentListCreateUpdateAPIView.as_view()),
    path("orders/market/", MarketOrderListCreateUpdateAPIView.as_view()),
    path("orders/limit/", LimitOrderListCreateUpdateAPIView.as_view()),
    path("portfolios/", InvestmentPortfolioListCreateUpdateAPIView.as_view()),
    path(
        "portfolios/<int:pk>/trades/", InvestmentPortfolioTradeRetrieveAPIView.as_view()
    ),
    path("trades/", TradeListCreateUpdateAPIView.as_view()),
    path("recommendations/", RecommendationListCreateUpdateAPIView.as_view()),
]
