from brokers.models import Investment, OrderActivatedStatuses, OrderStatuses
from brokers.utils import InvestmentService, LimitOrderService, TradeMaker
from django.db import IntegrityError
from django.db.models import Q


class LimitOrderTrade:
    """Make executable limit orders"""

    def make_orders(self) -> None:
        order_service = LimitOrderService()

        result = order_service.get_group_by_investment()

        investments = InvestmentService().get_by_filters(
            id__in=[item["investment"] for item in result], quantity__gt=0
        )

        trade_maker = TradeMaker()
        completed_orders = []
        for investment in investments:
            orders = self.__get_orders(investment)

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

    def __get_orders(self, investment: Investment):
        """Return executable limit orders"""
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
