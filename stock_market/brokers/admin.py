from brokers.models import (
    Investment,
    InvestmentPortfolio,
    LimitOrder,
    MarketOrder,
    Recommendation,
    Trade,
)
from django.contrib import admin

admin.site.register(
    [Investment, MarketOrder, LimitOrder, InvestmentPortfolio, Trade, Recommendation]
)
