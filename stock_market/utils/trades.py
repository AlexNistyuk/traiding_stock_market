import abc

from brokers.models import (
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
    def get_sell_order(self, *args, **kwargs):
        ...

    @abc.abstractmethod
    def get_buy_order(self, *args, **kwargs):
        ...


class MarketOrderTrade(IOrder):
    def __get_queryset(self, target_order: MarketOrder | LimitOrder, is_sell: bool):
        return (
            MarketOrder.objects.filter(
                quantity=target_order.quantity,
                is_sell=is_sell,
                investment=target_order.investment,
                status=OrderStatuses.ACTIVE,
            )
            .exclude(portfolio=target_order.portfolio)
            .select_related("investment", "portfolio__owner")
            .first()
        )

    def get_sell_order(self, target_order: MarketOrder | LimitOrder):
        return self.__get_queryset(target_order, is_sell=True)

    def get_buy_order(self, target_order: MarketOrder | LimitOrder):
        return self.__get_queryset(target_order, is_sell=False)


class LimitOrderTrade(IOrder):
    status_reverse_map = {
        OrderActivatedStatuses.LTE: OrderActivatedStatuses.GTE,
        OrderActivatedStatuses.LT: OrderActivatedStatuses.GT,
        OrderActivatedStatuses.GTE: OrderActivatedStatuses.LTE,
        OrderActivatedStatuses.GT: OrderActivatedStatuses.LT,
    }

    def __get_queryset(self, target_order: MarketOrder | LimitOrder, is_sell: bool):
        if is_sell:
            queryset_filters = [
                OrderActivatedStatuses.LTE,
                OrderActivatedStatuses.LT,
                OrderActivatedStatuses.GTE,
                OrderActivatedStatuses.GT,
            ]
        else:
            queryset_filters = [
                OrderActivatedStatuses.GTE,
                OrderActivatedStatuses.GT,
                OrderActivatedStatuses.LTE,
                OrderActivatedStatuses.LT,
            ]

        investment = target_order.investment
        price_field = "price__"
        first_expression = Q((price_field + queryset_filters[0], investment.price)) & Q(
            activated_status__in=[
                OrderActivatedStatuses.EQUAL,
                self.status_reverse_map[queryset_filters[0]],
            ]
        )
        second_expression = Q(
            (price_field + queryset_filters[1], investment.price)
        ) & Q(activated_status=self.status_reverse_map[queryset_filters[1]])
        third_expression = Q((price_field + queryset_filters[2], investment.price)) & Q(
            activated_status=self.status_reverse_map[queryset_filters[2]]
        )
        fourth_expression = Q(
            (price_field + queryset_filters[3], investment.price)
        ) & Q(activated_status=self.status_reverse_map[queryset_filters[3]])

        orders = (
            LimitOrder.objects.filter(
                Q(
                    is_sell=is_sell,
                    quantity=target_order.quantity,
                    status=OrderStatuses.ACTIVE,
                )
                & (
                    first_expression
                    | second_expression
                    | third_expression
                    | fourth_expression
                )
            )
            .exclude(portfolio=target_order.portfolio)
            .select_related("investment", "portfolio")
        )

        return orders

    def get_sell_order(self, target_order: MarketOrder | LimitOrder):
        return self.__get_queryset(target_order, is_sell=True)

    def get_buy_order(self, target_order: MarketOrder | LimitOrder):
        return self.__get_queryset(target_order, is_sell=False)


class Trade:
    def make(self, sell_order, buy_order):
        try:
            with transaction.atomic():
                spend_amount = buy_order.investment.price * buy_order.quantity

                buy_order.portfolio.owner.balance -= spend_amount

                buy_order.portfolio.quantity += buy_order.quantity
                buy_order.portfolio.spend_amount += buy_order.spend_amount

                sell_order.portfolio.owner.balance += spend_amount

                sell_order.status = OrderStatuses.COMPLETED
                buy_order.status = OrderStatuses.COMPLETED

                TradeModel.objects.create(
                    quantity=sell_order.quantity,
                    price=sell_order.investment.price,
                    investment=sell_order.investment,
                    buyer=buy_order.portfolio,
                    seller=sell_order.portfolio,
                )

                buy_order.portfolio.owner.save()
                buy_order.portfolio.save()
                sell_order.portfolio.owner.save()
                sell_order.save()
                buy_order.save()
        except IntegrityError:
            ...
