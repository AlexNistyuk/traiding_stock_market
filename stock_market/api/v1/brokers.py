from brokers.views import (
    InvestmentPortfolioViewSet,
    InvestmentViewSet,
    LimitOrderViewSet,
    MarketOrderViewSet,
    RecommendationViewSet,
    TradeViewSet,
)
from rest_framework.routers import DefaultRouter

investment_router = DefaultRouter()
investment_router.register(r"investments", InvestmentViewSet)

market_order_router = DefaultRouter()
market_order_router.register(r"orders/market", MarketOrderViewSet)

limit_order_router = DefaultRouter()
limit_order_router.register(r"orders/limit", LimitOrderViewSet)

investment_portfolio_router = DefaultRouter()
investment_portfolio_router.register(r"portfolios", InvestmentPortfolioViewSet)

trade_router = DefaultRouter()
trade_router.register(r"trades", TradeViewSet)

recommendation_router = DefaultRouter()
recommendation_router.register(r"recommendations", RecommendationViewSet)

urlpatterns = investment_router.urls
urlpatterns += market_order_router.urls
urlpatterns += limit_order_router.urls
urlpatterns += investment_portfolio_router.urls
urlpatterns += trade_router.urls
urlpatterns += recommendation_router.urls
