import smtplib
from email.mime.text import MIMEText

from brokers.models import LimitOrder, OrderStatuses
from brokers.utils import (
    InvestmentService,
    LimitOrderService,
    LimitOrderTrade,
    TradeMaker,
)
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

    send_mass_mail(completed_orders)


def send_mail(recipient: str):
    with Email() as email:
        email.send_welcome_mail(recipient)


def send_mass_mail(orders: list[LimitOrder]):
    with Email() as email:
        email.send_executed_orders(orders)


class Email:
    subject = "Trade Platform"
    sender = settings.EMAIL_HOST_USER

    def __enter__(self):
        self.server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        self.server.starttls()
        self.server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.quit()

    def send_welcome_mail(self, recipient: str):
        message = """
        Hi! You have been successfully registered!
        Thank you for choosing our trade platform
        """

        message = self.__get_message_as_string(message, recipient)

        self.server.sendmail(self.sender, recipient, message)

    def send_executed_orders(self, orders: list[LimitOrder]):
        message_template = "Hey! You have bought %s!"
        messages = [
            self.__get_message_as_string(
                message_template % order.investment.name, order.portfolio.owner.email
            )
            for order in orders
        ]

        [
            self.server.sendmail(self.sender, order.portfolio.owner.email, message)
            for message, order in zip(messages, orders)
        ]

    def __get_message_as_string(self, message: str, recipient: str) -> str:
        message = MIMEText(message)
        message["Subject"] = self.subject
        message["From"] = self.sender
        message["To"] = recipient

        return message.as_string()
