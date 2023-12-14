from brokers.models import (
    Investment,
    InvestmentPortfolio,
    LimitOrder,
    MarketOrder,
    Recommendation,
    Trade,
)
from rest_framework import serializers


class InvestmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = (
            "name",
            "image",
            "price",
            "count",
            "type",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "created_at",
            "updated_at",
        )


class InvestmentRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = (
            "name",
            "image",
            "price",
            "count",
            "type",
            "created_at",
            "updated_at",
        )


class InvestmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = (
            "name",
            "image",
            "price",
            "count",
            "type",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "created_at",
            "updated_at",
        )


class MarketOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketOrder
        fields = (
            "count",
            "status",
            "is_sell",
            "owner",
            "investment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "status",
            "created_at",
            "updated_at",
        )


class MarketOrderRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketOrder
        fields = (
            "count",
            "status",
            "is_sell",
            "owner",
            "investment",
            "created_at",
            "updated_at",
        )


class MarketOrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketOrder
        fields = (
            "count",
            "status",
            "is_sell",
            "owner",
            "investment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "created_at",
            "updated_at",
        )


class LimitOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimitOrder
        fields = (
            "price",
            "activated_status",
            "count",
            "status",
            "is_sell",
            "owner",
            "investment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "status" "created_at",
            "updated_at",
        )


class LimitOrderRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimitOrder
        fields = (
            "price",
            "activated_status",
            "count",
            "status",
            "is_sell",
            "owner",
            "investment",
            "created_at",
            "updated_at",
        )


class LimitOrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimitOrder
        fields = (
            "price",
            "activated_status",
            "count",
            "status",
            "is_sell",
            "owner",
            "investment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "created_at",
            "updated_at",
        )


class InvestmentPortfolioCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPortfolio
        fields = (
            "count",
            "spend_amount",
            "owner",
            "investment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "spend_amount",
            "created_at",
            "updated_at",
        )


class InvestmentPortfolioRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPortfolio
        fields = (
            "count",
            "spend_amount",
            "owner",
            "investment",
            "created_at",
            "updated_at",
        )


class InvestmentPortfolioUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPortfolio
        fields = (
            "count",
            "spend_amount",
            "owner",
            "investment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "spend_amount",
            "created_at",
            "updated_at",
        )


class TradeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = (
            "count",
            "price",
            "seller",
            "buyer",
            "investment",
            "created_at",
        )

        read_only_fields = ("created_at",)


class TradeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = (
            "count",
            "price",
            "seller",
            "buyer",
            "investment",
            "created_at",
        )


class TradeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = (
            "count",
            "price",
            "seller",
            "buyer",
            "investment",
            "created_at",
        )

        read_only_fields = ("created_at",)


class RecommendationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = (
            "counter",
            "investment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "created_at",
            "updated_at",
        )


class RecommendationRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = (
            "counter",
            "investment",
            "created_at",
            "updated_at",
        )


class RecommendationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = (
            "counter",
            "investment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "created_at",
            "updated_at",
        )
