from brokers.models import (Investment, InvestmentPortfolio, LimitOrder,
                            MarketOrder, Trade)
from rest_framework import serializers


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = "__all__"


class MarketOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketOrder
        fields = "__all__"


class LimitOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimitOrder
        fields = "__all__"


class InvestmentPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPortfolio
        fields = "__all__"


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = "__all__"
