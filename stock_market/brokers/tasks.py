import smtplib
from email.message import EmailMessage

from brokers.models import Investment, LimitOrder, OrderActivatedStatuses, OrderStatuses
from brokers.utils import (
    InvestmentService,
    InvestmentUpdateService,
    LimitOrderService,
    TradeMaker,
)
from django.db import IntegrityError
from django.db.models import Q

from stock_market import celery_app, settings


class MessageBrokerHandler:
    """Handle messages from message brokers"""

    @staticmethod
    @celery_app.task
    def handle(tickers: list[dict]):
        InvestmentUpdateService().update(tickers)
        LimitOrderTrade().make_orders()


class LimitOrderTrade:
    """Make executable limit orders"""

    @staticmethod
    @celery_app.task
    def make_orders() -> None:
        order_service = LimitOrderService()

        result = order_service.get_group_by_investment()

        investments = InvestmentService().get_by_filters(
            id__in=[item["investment"] for item in result], quantity__gt=0
        )

        trade_maker = TradeMaker()
        completed_orders = []
        for investment in investments:
            orders = LimitOrderTrade.__get_orders(investment)

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
        Sender.send_mass_mail.delay(completed_orders)

    @staticmethod
    def __get_orders(investment: Investment):
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


class Sender:
    """Send messages on emails"""

    @staticmethod
    @celery_app.task
    def send_mass_mail(orders: list[LimitOrder]):
        with Email() as email:
            email.send_executed_orders(orders)

    @staticmethod
    @celery_app.task
    def send_mail(recipient: str):
        with Email() as email:
            email.send_welcome_mail(recipient)


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

    def __get_welcome_message(self):
        return """
        Hi! You have been successfully registered!
        Thank you for choosing our trade platform
        """

    def send_welcome_mail(self, recipient: str):
        welcome_message = self.__get_welcome_message()
        message = self.__get_email_message(welcome_message, recipient)
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
