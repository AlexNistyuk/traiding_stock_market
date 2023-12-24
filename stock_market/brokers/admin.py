from brokers.models import (
    Investment,
    InvestmentPortfolio,
    LimitOrder,
    MarketOrder,
    Recommendation,
    Trade,
)
from django.contrib import admin

admin.site.register(Investment)
admin.site.register(MarketOrder)
admin.site.register(LimitOrder)
admin.site.register(InvestmentPortfolio)
admin.site.register(Trade)
admin.site.register(Recommendation)
