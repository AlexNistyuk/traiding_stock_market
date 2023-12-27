import abc

from brokers.models import (
    Investment,
    InvestmentPortfolio,
    LimitOrder,
    MarketOrder,
    OrderActivatedStatuses,
    OrderStatuses,
    Trade,
)
from django.db import IntegrityError, transaction
from django.db.models import Count, F, Q
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


class IOrder(abc.ABC):
    @abc.abstractmethod
    def get_orders(self, *args, **kwargs):
        raise NotImplementedError


class MarketOrderTrade(IOrder):
    def get_orders(self, investment: Investment):
        return MarketOrderService().get_by_filters(
            status=OrderStatuses.ACTIVE,
            quantity__lte=investment.quantity,
            investment=investment,
        )


class LimitOrderTrade(IOrder):
    def get_orders(self, investment: Investment):
        return LimitOrderService().get_by_filters(
            Q(
                investment=investment,
                status=OrderStatuses.ACTIVE,
                quantity__lte=investment.quantity,
            )
            & (
                Q(
                    price__gte=investment.price,
                    activated_status__in=[
                        OrderActivatedStatuses.LTE,
                        OrderActivatedStatuses.EQUAL,
                    ],
                )
                | Q(
                    price__gt=investment.price,
                    activated_status=OrderActivatedStatuses.LT,
                )
                | Q(
                    price__lte=investment.price,
                    activated_status=OrderActivatedStatuses.GTE,
                )
                | Q(
                    price__lt=investment.price,
                    activated_status=OrderActivatedStatuses.GT,
                )
            )
        )


class TradeMaker:
    def make(self, order: MarketOrder | LimitOrder, investment: Investment):
        with transaction.atomic():
            spend_money = investment.price * order.quantity

            order.portfolio.owner.balance = F("balance") - spend_money
            order.portfolio.spend_amount += spend_money

            order.portfolio.quantity += order.quantity
            investment.quantity = F("quantity") - order.quantity

            order.status = OrderStatuses.COMPLETED

            trade = {
                "quantity": order.quantity,
                "portfolio": order.portfolio,
            }

            order.portfolio.owner.save()
            order.portfolio.save()
            order.save()
            investment.save()
            TradeService(trade).create()

    def make_market_order(self, market_order: MarketOrder):
        if market_order.status != OrderStatuses.ACTIVE:
            return market_order
        if market_order.quantity > market_order.investment.quantity:
            return market_order

        try:
            self.make(market_order, market_order.investment)
        except IntegrityError:
            ...
        else:
            market_order.refresh_from_db()

        return market_order

    def make_limit_order(self, limit_order: LimitOrder):
        if not self.__is_executable_limit_order(limit_order):
            return limit_order

        try:
            self.make(limit_order, limit_order.investment)
        except IntegrityError:
            ...
        else:
            limit_order.refresh_from_db()

        return limit_order

    def __is_executable_limit_order(self, limit_order: LimitOrder):
        investment = limit_order.investment
        order_price = limit_order.price
        order_status = limit_order.status
        investment_price = investment.price

        if order_status != OrderStatuses.ACTIVE:
            return False
        if limit_order.quantity > limit_order.investment.quantity:
            return False
        if order_price >= investment_price and order_status in (
            OrderActivatedStatuses.LTE,
            OrderActivatedStatuses.EQUAL,
        ):
            return True
        if order_price < investment_price and order_status == OrderActivatedStatuses.LT:
            return True
        if (
            order_price <= investment_price
            and order_status == OrderActivatedStatuses.GTE
        ):
            return True
        if order_price < investment_price and order_status == OrderActivatedStatuses.GT:
            return True
        return False
