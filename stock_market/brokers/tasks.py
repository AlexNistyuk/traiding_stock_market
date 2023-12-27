from brokers.utils import (
    InvestmentService,
    IOrder,
    LimitOrderService,
    LimitOrderTrade,
    MarketOrderService,
    MarketOrderTrade,
    OrderService,
    Trade,
)
from django.db import IntegrityError


def orders_trade(order_service: OrderService, order_trade: IOrder):
    result = order_service.get_group_by_investment()

    investments = InvestmentService().get_by_filters(
        id__in=[item["investment"] for item in result], quantity__gt=0
    )

    for investment in investments:
        orders = order_trade.get_orders(investment)

        for order in orders:
            try:
                Trade().make(order, investment)
            except IntegrityError:
                ...
            else:
                investment.refresh_from_db()
                if investment.quantity == 0:
                    break


def limit_orders_trade():
    order_service = LimitOrderService()
    order_trade = LimitOrderTrade()

    return orders_trade(order_service, order_trade)


def market_orders_trade():
    order_service = MarketOrderService()
    order_trade = MarketOrderTrade()

    return orders_trade(order_service, order_trade)
