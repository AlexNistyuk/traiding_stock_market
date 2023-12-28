from brokers.models import OrderStatuses
from brokers.utils import (
    InvestmentService,
    LimitOrderService,
    LimitOrderTrade,
    TradeMaker,
)
from django.db import IntegrityError


def limit_orders_trade() -> None:
    """Trades with executable limit orders"""
    order_service = LimitOrderService()
    order_trade = LimitOrderTrade()

    result = order_service.get_group_by_investment()

    investments = InvestmentService().get_by_filters(
        id__in=[item["investment"] for item in result], quantity__gt=0
    )

    trade_maker = TradeMaker()
    completed_orders = []
    for investment in investments:
        orders = order_trade.get_orders(investment)

        for i, order in enumerate(orders):
            try:
                trade_maker.make(order.quantity, order.portfolio, investment)
            except IntegrityError:
                continue

            order.status = OrderStatuses.COMPLETED
            completed_orders.append(order)

            if i < len(orders) - 1:
                investment.refresh_from_db()
                if investment.quantity == 0:
                    break

    order_service.bulk_update(completed_orders, ("status",))
