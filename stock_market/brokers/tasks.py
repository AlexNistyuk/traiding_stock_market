from brokers.models import LimitOrder, OrderStatuses
from brokers.utils import (
    InvestmentService,
    LimitOrderService,
    LimitOrderTrade,
    TradeMaker,
)
from django.core.mail import send_mail, send_mass_mail
from django.db import IntegrityError

from stock_market import settings


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
    Email().send_executed_orders(completed_orders)


class Email:
    subject = "Trade Platform"
    sender = settings.EMAIL_HOST_USER

    def send_welcome_email(self, recipient: str):
        message = """
        Hi! You have been successfully registered!
        Thank you for choosing our trade platform
        """

        send_mail(self.subject, message, self.sender, (recipient,))

    def send_executed_orders(self, orders: list[LimitOrder]):
        message_template = "Hey! You have bought %s!"
        data = [
            (
                self.subject,
                message_template % order.investment.name,
                self.sender,
                (order.portfolio.owner.email,),
            )
            for order in orders
        ]

        send_mass_mail(data)
