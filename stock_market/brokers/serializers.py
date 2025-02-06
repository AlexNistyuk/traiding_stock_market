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
            "id",
            "name",
            "image",
            "price",
            "quantity",
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
            "id",
            "name",
            "image",
            "price",
            "quantity",
            "type",
            "created_at",
            "updated_at",
        )


class InvestmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = (
            "id",
            "name",
            "image",
            "price",
            "quantity",
            "type",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "name",
            "created_at",
            "updated_at",
        )


class MarketOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketOrder
        fields = (
            "id",
            "quantity",
            "status",
            "portfolio",
            "investment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "status",
            "investment",
            "created_at",
            "updated_at",
        )


class MarketOrderRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketOrder
        fields = (
            "id",
            "quantity",
            "status",
            "portfolio",
            "investment",
            "created_at",
            "updated_at",
        )


class MarketOrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketOrder
        fields = (
            "id",
            "quantity",
            "status",
            "portfolio",
            "investment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "portfolio",
            "investment",
            "created_at",
            "updated_at",
        )


class LimitOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimitOrder
        fields = (
            "id",
            "price",
            "activated_status",
            "quantity",
            "status",
            "portfolio",
            "investment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "status",
            "investment",
            "created_at",
            "updated_at",
        )


class LimitOrderRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimitOrder
        fields = (
            "id",
            "price",
            "activated_status",
            "quantity",
            "status",
            "portfolio",
            "investment",
            "created_at",
            "updated_at",
        )


class LimitOrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimitOrder
        fields = (
            "id",
            "price",
            "activated_status",
            "quantity",
            "status",
            "portfolio",
            "investment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "portfolio",
            "investment",
            "created_at",
            "updated_at",
        )


class InvestmentPortfolioCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPortfolio
        fields = (
            "id",
            "quantity",
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
            "id",
            "quantity",
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
            "id",
            "quantity",
            "spend_amount",
            "owner",
            "investment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "investment",
            "owner",
            "spend_amount",
            "created_at",
            "updated_at",
        )


class TradeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = (
            "id",
            "quantity",
            "price",
            "portfolio",
            "investment",
            "created_at",
        )

        read_only_fields = (
            "created_at",
            "price",
            "investment",
        )


class TradeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = (
            "id",
            "quantity",
            "price",
            "portfolio",
            "investment",
            "created_at",
        )


class TradeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = (
            "id",
            "quantity",
            "price",
            "portfolio",
            "investment",
            "created_at",
        )

        read_only_fields = ("created_at", "price", "investment")


class RecommendationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = (
            "id",
            "percentage",
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
            "id",
            "percentage",
            "investment",
            "created_at",
            "updated_at",
        )


class RecommendationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = (
            "id",
            "percentage",
            "investment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "investment",
            "created_at",
            "updated_at",
        )
