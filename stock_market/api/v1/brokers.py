from brokers.views import (
    InvestmentListCreateAPIView,
    InvestmentPortfolioCreateAPIView,
    InvestmentPortfolioRetrieveUpdateAPIView,
    InvestmentPortfolioTradeRetrieveAPIView,
    InvestmentRetrieveUpdateAPIView,
    LimitOrderListCreateAPIView,
    LimitOrderRetrieveUpdateAPIView,
    MarketOrderListCreateAPIView,
    MarketOrderRetrieveUpdateAPIView,
    RecommendationListCreateAPIView,
    RecommendationRetrieveUpdateAPIView,
    TradeListCreateAPIView,
    TradeRetrieveUpdateAPIView,
)
from django.urls import path

urlpatterns = [
    path("investments/", InvestmentListCreateAPIView.as_view()),
    path("investments/<int:pk>/", InvestmentRetrieveUpdateAPIView.as_view()),
    path("orders/market/", MarketOrderListCreateAPIView.as_view()),
    path("orders/market/<int:pk>/", MarketOrderRetrieveUpdateAPIView.as_view()),
    path("orders/limit/", LimitOrderListCreateAPIView.as_view()),
    path("orders/limit/<int:pk>/", LimitOrderRetrieveUpdateAPIView.as_view()),
    path("portfolio/", InvestmentPortfolioCreateAPIView.as_view()),
    path("portfolio/<int:pk>/", InvestmentPortfolioRetrieveUpdateAPIView.as_view()),
    path(
        "portfolio/<int:pk>/trades/", InvestmentPortfolioTradeRetrieveAPIView.as_view()
    ),
    path("trades/", TradeListCreateAPIView.as_view()),
    path("trades/<int:pk>/", TradeRetrieveUpdateAPIView.as_view()),
    path("recommendations/", RecommendationListCreateAPIView.as_view()),
    path("recommendations/<int:pk>/", RecommendationRetrieveUpdateAPIView.as_view()),
]
