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
            "count",
            "type",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
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
            "count",
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
            "count",
            "type",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class MarketOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketOrder
        fields = (
            "id",
            "count",
            "status",
            "is_sell",
            "owner",
            "investment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "status",
            "created_at",
            "updated_at",
        )


class MarketOrderRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketOrder
        fields = (
            "id",
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
            "id",
            "count",
            "status",
            "is_sell",
            "owner",
            "investment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
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
            "count",
            "status",
            "is_sell",
            "owner",
            "investment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "status",
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
            "id",
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
            "id",
            "created_at",
            "updated_at",
        )


class InvestmentPortfolioCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPortfolio
        fields = (
            "id",
            "count",
            "spend_amount",
            "owner",
            "investment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "spend_amount",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        validated_data["spend_amount"] = (
            validated_data["count"] * validated_data["investment"].price
        )

        return InvestmentPortfolio.objects.create(**validated_data)


class InvestmentPortfolioRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPortfolio
        fields = (
            "id",
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
            "id",
            "count",
            "spend_amount",
            "owner",
            "investment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "spend_amount",
            "created_at",
            "updated_at",
        )


class TradeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = (
            "id",
            "count",
            "price",
            "seller",
            "buyer",
            "investment",
            "created_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "price",
        )

    def create(self, validated_data):
        validated_data["price"] = validated_data["investment"].price

        return Trade.objects.create(**validated_data)


class TradeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = (
            "id",
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
            "id",
            "count",
            "price",
            "seller",
            "buyer",
            "investment",
            "created_at",
        )

        read_only_fields = ("id", "created_at", "price")

    def update(self, instance, validated_data):
        instance.count = validated_data["count"]
        instance.seller = validated_data["seller"]
        instance.buyer = validated_data["buyer"]
        instance.investment = validated_data["investment"]
        instance.price = validated_data["investment"].price
        instance.save()

        return instance


class RecommendationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = (
            "id",
            "counter",
            "investment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class RecommendationRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = (
            "id",
            "counter",
            "investment",
            "created_at",
            "updated_at",
        )


class RecommendationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = (
            "id",
            "counter",
            "investment",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )
