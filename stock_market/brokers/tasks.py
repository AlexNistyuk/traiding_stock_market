import smtplib
from email.message import EmailMessage

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
    password = settings.EMAIL_HOST_PASSWORD

    def __enter__(self):
        self.server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
        self.server.login(self.sender, self.password)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.quit()

    def send_welcome_mail(self, recipient: str):
        message = """
        Hi! You have been successfully registered!
        Thank you for choosing our trade platform
        """

        message = self.__get_email_message(message, recipient)
        self.server.send_message(message)

    def send_executed_orders(self, orders: list[LimitOrder]):
        message_template = "Hey! You have bought %s!"
        messages = [
            self.__get_email_message(
                message_template % order.investment.name, order.portfolio.owner.email
            )
            for order in orders
        ]

        [self.server.send_message(message) for message in messages]

    def __get_email_message(self, message: str, recipient: str) -> EmailMessage:
        email = EmailMessage()
        email["Subject"] = self.subject
        email["From"] = self.sender
        email["To"] = recipient
        email.set_content(message)

        return email
