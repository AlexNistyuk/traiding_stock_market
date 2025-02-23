from decimal import Decimal
from math import ceil
from typing import Iterable

from brokers.models import (
    Investment,
    InvestmentPortfolio,
    InvestmentTypes,
    LimitOrder,
    MarketOrder,
    OrderActivatedStatuses,
    OrderStatuses,
    Recommendation,
    Trade,
)
from django.db import IntegrityError, transaction
from django.db.models import Count, F, QuerySet
from django.http import Http404
from utils.interfaces import IService


class InvestmentService(IService):
    def __init__(self, validated_data: dict = None, instance: Investment = None):
        self.data = validated_data
        self.instance = instance

    def get_by_filters(self, **filters):
        return Investment.objects.filter(**filters)

    def create(self):
        return Investment.objects.create(**self.data)

    def update(self):
        self.instance.image = self.data.get("image", self.instance.image)
        self.instance.price = self.data["price"]
        self.instance.quantity = self.data["quantity"]
        self.instance.type = self.data["type"]
        self.instance.save()

        return self.instance

    def get_by_id_or_404(self, investment_id: int):
        try:
            return Investment.objects.get(id=investment_id)
        except Investment.DoesNotExist:
            raise Http404

    def delete(self, investment: Investment):
        return investment.delete()

    def get_all(self):
        return Investment.objects.all()

    def bulk_create(self, investments: Iterable[Investment]):
        return Investment.objects.bulk_create(investments)

    def bulk_update(self, investments: Iterable[Investment], *args):
        return Investment.objects.bulk_update(investments, *args)

    def get_percentage(self, old_price: Decimal, new_price: Decimal):
        return ceil((new_price - old_price) / old_price * 100)


class InvestmentPortfolioService(IService):
    def __init__(
        self, validated_data: dict = None, instance: InvestmentPortfolio = None
    ):
        self.data = validated_data
        self.instance = instance

    def create(self):
        self.data["spend_amount"] = (
            self.data["investment"].price * self.data["quantity"]
        )

        return InvestmentPortfolio.objects.create(**self.data)

    def update(self):
        count_difference = self.data["quantity"] - self.instance.quantity
        self.instance.spend_amount += self.instance.investment.price * count_difference

        self.instance.quantity = self.data["quantity"]
        self.instance.save()

        return self.instance

    def get_by_id_or_404(self, portfolio_id: int):
        try:
            return InvestmentPortfolio.objects.select_related("owner").get(
                id=portfolio_id
            )
        except InvestmentPortfolio.DoesNotExist:
            raise Http404

    def delete(self, portfolio: InvestmentPortfolio):
        return portfolio.delete()

    def get_all(self):
        return InvestmentPortfolio.objects.select_related("owner").all()

    def bulk_create(self, portfolios: Iterable[InvestmentPortfolio]):
        return InvestmentPortfolio.objects.bulk_create(portfolios)

    def bulk_update(self, portfolios: Iterable[InvestmentPortfolio]):
        return InvestmentPortfolio.objects.bulk_update(portfolios)

    def get_by_filters(self, **filters):
        return InvestmentPortfolio.objects.select_related("owner").filter(**filters)

    def get_by_filters_and_values(self, *values, **filters):
        return (
            InvestmentPortfolio.objects.select_related("owner")
            .filter(**filters)
            .values(*values)
        )


class OrderService(IService):
    model: MarketOrder | LimitOrder = None

    def __init__(
        self, validated_data: dict = None, instance: MarketOrder | LimitOrder = None
    ):
        self.data = validated_data
        self.instance = instance

    def create(self):
        self.data["investment"] = self.data["portfolio"].investment

        return self.model.objects.create(**self.data)

    def get_by_id_or_404(self, order_id: int):
        try:
            return self.model.objects.select_related(
                "investment", "portfolio__owner"
            ).get(id=order_id)
        except self.model.DoesNotExist:
            raise Http404

    def delete(self, order: MarketOrder | LimitOrder):
        return order.delete()

    def get_all(self):
        return self.model.objects.select_related("investment", "portfolio__owner").all()

    def bulk_create(self, orders: Iterable[MarketOrder | LimitOrder]):
        return self.model.objects.bulk_create(orders)

    def bulk_update(self, orders: Iterable[MarketOrder | LimitOrder], *args):
        return self.model.objects.bulk_update(orders, *args)

    def get_by_filters(self, *args, **filters):
        return self.model.objects.select_related(
            "portfolio__owner", "investment"
        ).filter(*args, **filters)


class MarketOrderService(OrderService):
    model = MarketOrder

    def update(self):
        self.instance.quantity = self.data["quantity"]
        self.instance.status = self.data["status"]
        self.instance.save()

        return self.instance


class LimitOrderService(OrderService):
    model = LimitOrder

    def update(self):
        self.instance.quantity = self.data["quantity"]
        self.instance.status = self.data["status"]
        self.instance.price = self.data["price"]
        self.instance.activated_status = self.data["activated_status"]
        self.instance.save()

        return self.instance

    def get_group_by_investment(self):
        return (
            self.model.objects.values("investment")
            .annotate(count=Count("id"))
            .filter(status=OrderStatuses.ACTIVE)
        )


class TradeService(IService):
    def __init__(self, validated_data: dict = None, instance: Trade = None):
        self.data = validated_data
        self.instance = instance

    def create(self):
        self.data["investment"] = self.data["portfolio"].investment
        self.data["price"] = self.data["investment"].price

        return Trade.objects.create(**self.data)

    def update(self):
        self.instance.quantity = self.data["quantity"]
        self.instance.portfolio = self.data["portfolio"]
        self.instance.investment = self.data["portfolio"].investment
        self.instance.price = self.instance.investment.price
        self.instance.save()

        return self.instance

    def get_by_id_or_404(self, trade_id: int):
        try:
            return Trade.objects.select_related("investment", "portfolio__owner").get(
                id=trade_id
            )
        except Trade.DoesNotExist:
            raise Http404

    def delete(self, trade: Trade):
        return trade.delete()

    def get_all(self):
        return Trade.objects.select_related("investment", "portfolio__owner").all()

    def bulk_create(self, trades: Iterable[Trade]):
        return Trade.objects.bulk_create(trades)

    def bulk_update(self, trades: Iterable[Trade]):
        return Trade.objects.bulk_update(trades)

    def get_by_filters(self, **filters):
        return Trade.objects.select_related("investment", "portfolio__owner").filter(
            **filters
        )


class RecommendationService(IService):
    def __init__(self, validated_data: dict = None, instance: Recommendation = None):
        self.data = validated_data
        self.instance = instance

    def create(self):
        self.data["investment"] = self.data["investment"]

        return Recommendation.objects.create(**self.data)

    def update(self):
        self.instance.percentage = self.data["percentage"]
        self.instance.save()

        return self.instance

    def get_by_id_or_404(self, recommendation_id: int):
        try:
            return Recommendation.objects.get(id=recommendation_id)
        except Recommendation.DoesNotExist:
            raise Http404

    def delete(self, recommendation: Recommendation):
        return recommendation.delete()

    def get_all(self):
        return Recommendation.objects.select_related("investment").all()

    def bulk_create(self, recommendations: Iterable[Recommendation]):
        return Recommendation.objects.bulk_create(recommendations)

    def bulk_update(self, recommendations: Iterable[Recommendation], *args):
        return Recommendation.objects.bulk_update(recommendations, *args)

    def get_by_filters(self, **filters):
        return Recommendation.objects.select_related("investment").filter(**filters)

    def get_or_create(self, **filters):
        return Recommendation.objects.get_or_create(**filters)


class TradeMaker:
    def make(
        self, quantity: int, portfolio: InvestmentPortfolio, investment: Investment
    ):
        with transaction.atomic():
            spend_money = investment.price * quantity

            portfolio.owner.balance = F("balance") - spend_money
            portfolio.spend_amount += spend_money

            portfolio.quantity += quantity
            investment.quantity = F("quantity") - quantity

            trade = {
                "quantity": quantity,
                "portfolio": portfolio,
            }

            portfolio.owner.save()
            portfolio.save()
            investment.save()
            TradeService(trade).create()

    def make_market_order(self, quantity: int, portfolio: InvestmentPortfolio) -> bool:
        try:
            self.make(quantity, portfolio, portfolio.investment)
        except IntegrityError:
            return False
        return True

    def make_limit_order(self, limit_order: LimitOrder):
        if not self.__is_executable_limit_order(limit_order):
            return limit_order

        try:
            self.make(
                limit_order.quantity, limit_order.portfolio, limit_order.investment
            )
        except IntegrityError:
            ...
        else:
            limit_order.status = OrderStatuses.COMPLETED
            limit_order.save()

        return limit_order

    def __is_executable_limit_order(self, limit_order: LimitOrder):
        investment = limit_order.investment
        investment_price = investment.price

        order_price = limit_order.price
        order_activated_status = limit_order.activated_status

        if limit_order.quantity > investment.quantity:
            return False

        if order_price >= investment_price and order_activated_status in (
            OrderActivatedStatuses.LTE,
            OrderActivatedStatuses.EQUAL,
        ):
            return True

        if (
            order_price < investment_price
            and order_activated_status == OrderActivatedStatuses.LT
        ):
            return True

        if (
            order_price <= investment_price
            and order_activated_status == OrderActivatedStatuses.GTE
        ):
            return True

        if (
            order_price < investment_price
            and order_activated_status == OrderActivatedStatuses.GT
        ):
            return True
        return False


class InvestmentUpdateService:
    """Update investments and recommendations"""

    investment_service = InvestmentService()
    recommendation_service = RecommendationService()

    def update(self, tickers: Iterable[dict]):
        tickers = self.__change_tickers(tickers)
        investments_names = tickers.keys()

        recommendations = self.recommendation_service.get_by_filters(
            investment__name__in=investments_names
        )
        existed_investments = [
            recommendation.investment.name for recommendation in recommendations
        ]
        create_investments = set(investments_names) - set(existed_investments)

        if create_investments:
            self.__create(tickers, create_investments)
        if existed_investments:
            self.__update(tickers, recommendations)

    def __update(self, tickers: dict, recommendations: QuerySet):
        updated_investments = []

        for recommendation in recommendations:
            investment = recommendation.investment
            investment.price = tickers[investment.name]["best_bid_price"]
            recommendation.percentage = tickers[investment.name]["price_change_percent"]

            updated_investments.append(investment)

        self.investment_service.bulk_update(updated_investments, ["price"])
        self.recommendation_service.bulk_update(recommendations, ["percentage"])

    def __create(self, tickers: dict, create_investments: set):
        created_investments = []
        created_recommendations = []

        for investment_name in create_investments:
            new_investment = Investment(
                name=investment_name,
                price=tickers[investment_name]["best_bid_price"],
                type=InvestmentTypes.CRYPTOCURRENCY,
            )
            new_recommendation = Recommendation(
                investment=new_investment,
                percentage=tickers[investment_name]["price_change_percent"],
            )

            created_investments.append(new_investment)
            created_recommendations.append(new_recommendation)

        self.investment_service.bulk_create(created_investments)
        self.recommendation_service.bulk_create(created_recommendations)

    def __change_tickers(self, tickers: Iterable[dict]) -> dict:
        new_tickers = {}
        for ticker in tickers:
            new_tickers[ticker["symbol"]] = {
                "best_bid_price": Decimal(ticker["best_bid_price"]),
                "price_change_percent": ticker["price_change_percent"],
            }

        return new_tickers
