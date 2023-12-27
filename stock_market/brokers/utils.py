from brokers.models import (
    Investment,
    InvestmentPortfolio,
    LimitOrder,
    MarketOrder,
    OrderStatuses,
    Trade,
)
from django.db.models import Count
from django.http import Http404
from users.utils import IService


class InvestmentService:
    def get_by_filters(self, **filters):
        return Investment.objects.filter(**filters)


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

    def bulk_create(self, portfolios: list[InvestmentPortfolio]):
        return InvestmentPortfolio.objects.bulk_create(portfolios)

    def bulk_update(self, portfolios: list[InvestmentPortfolio]):
        return InvestmentPortfolio.objects.bulk_update(portfolios)

    def get_by_filters(self, **filters):
        return InvestmentPortfolio.objects.select_related("owner").filter(**filters)


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
            return self.model.objects.select_related("investment", "portfolio").get(
                id=order_id
            )
        except self.model.DoesNotExist:
            raise Http404

    def delete(self, order: MarketOrder | LimitOrder):
        return order.delete()

    def get_all(self):
        return self.model.objects.select_related("investment", "portfolio").all()

    def bulk_create(self, orders: list[MarketOrder | LimitOrder]):
        return self.model.objects.bulk_create(orders)

    def bulk_update(self, orders: list[MarketOrder | LimitOrder]):
        return self.model.objects.bulk_update(orders)

    def get_by_filters(self, *args, **filters):
        return self.model.objects.select_related("portfolio", "investment").filter(
            *args, **filters
        )

    def get_group_by_investment(self):
        return (
            self.model.objects.values("investment")
            .annotate(count=Count("id"))
            .filter(status=OrderStatuses.ACTIVE)
        )


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
            return Trade.objects.select_related("investment", "portfolio").get(
                id=trade_id
            )
        except Trade.DoesNotExist:
            raise Http404

    def delete(self, trade: Trade):
        return trade.delete()

    def get_all(self):
        return Trade.objects.select_related("investment", "portfolio").all()

    def bulk_create(self, trades: list[Trade]):
        return Trade.objects.bulk_create(trades)

    def bulk_update(self, trades: list[Trade]):
        return Trade.objects.bulk_update(trades)

    def get_by_filters(self, **filters):
        return Trade.objects.select_related("investment", "portfolio").filter(**filters)
