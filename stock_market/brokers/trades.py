import abc

from brokers.models import (
    Investment,
    LimitOrder,
    MarketOrder,
    OrderActivatedStatuses,
    OrderStatuses,
)
from brokers.utils import LimitOrderService, MarketOrderService, TradeService
from django.db import IntegrityError, transaction
from django.db.models import F, Q


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


class Trade:
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
            Trade().make(market_order, market_order.investment)
        except IntegrityError:
            ...
        else:
            market_order.refresh_from_db()

        return market_order

    def make_limit_order(self, limit_order: LimitOrder):
        if not self.__is_executable_limit_order(limit_order):
            return limit_order

        try:
            Trade().make(limit_order, limit_order.investment)
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
