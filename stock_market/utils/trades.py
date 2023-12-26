import abc

from brokers.models import (
    Investment,
    LimitOrder,
    MarketOrder,
    OrderActivatedStatuses,
    OrderStatuses,
)
from brokers.models import Trade as TradeModel
from django.db import IntegrityError, transaction
from django.db.models import Q


class IOrder(abc.ABC):
    @abc.abstractmethod
    def get_orders(self, *args, **kwargs):
        ...


class MarketOrderTrade(IOrder):
    def get_orders(self, investment: Investment):
        return MarketOrder.objects.filter(
            status=OrderStatuses.ACTIVE,
            quantity__lte=investment.quantity,
        ).select_related("investment", "portfolio")


class LimitOrderTrade(IOrder):
    def get_orders(self, investment: Investment):
        return LimitOrder.objects.filter(
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
        ).select_related("investment", "portfolio")


class Trade:
    def make(self, order: MarketOrder | LimitOrder):
        try:
            with transaction.atomic():
                spend_money = order.investment.price * order.quantity

                order.portfolio.owner.balance -= spend_money

                order.portfolio.spend_amount += spend_money
                order.portfolio.quantity += order.quantity

                order.status = OrderStatuses.COMPLETED

                TradeModel.objects.create(
                    quantity=order.quantity,
                    price=order.investment.price,
                    investment=order.investment,
                    portfolio=order.portfolio,
                )

                order.portfolio.owner.save()
                order.portfolio.save()
                order.save()
        except IntegrityError:
            ...
