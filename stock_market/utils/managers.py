import abc

from brokers.models import InvestmentPortfolio, LimitOrder, MarketOrder
from django.db import IntegrityError, transaction
from utils.exceptions import Http400


class IManager(abc.ABC):
    model = None

    def __init__(self, validated_data: dict, instance=None):
        self.data = validated_data
        self.instance = instance

    @abc.abstractmethod
    def create(self):
        ...

    @abc.abstractmethod
    def update(self):
        ...


class InvestmentPortfolioManager(IManager):
    model = InvestmentPortfolio

    def create(self):
        self.data["spend_amount"] = (
            self.data["investment"].price * self.data["quantity"]
        )

        return self.model.objects.create(**self.data)

    def update(self):
        count_difference = self.data["quantity"] - self.instance.quantity
        if count_difference > 0:
            self.instance.spend_amount += (
                self.instance.investment.price * count_difference
            )

        self.instance.quantity = self.data["quantity"]
        self.instance.save()

        return self.instance


class OrderManager(IManager):
    def create(self):
        portfolio = self.data["portfolio"]
        self.data["investment"] = portfolio.investment

        with transaction.atomic():
            self.change_portfolio_quantity(portfolio)

            return self.model.objects.create(**self.data)

    def change_portfolio_quantity(self, portfolio: InvestmentPortfolio):
        quantity = self.get_quantity_difference()
        if quantity == 0:
            return

        try:
            portfolio.quantity += quantity
            portfolio.save()
        except IntegrityError:
            raise Http400(
                {"detail": "The portfolio does not have the required quantity to sell"}
            )

    def get_quantity_difference(self) -> int:
        if self.instance is None:
            return -self.data["quantity"] if self.data["is_sell"] else 0

        if self.instance.is_sell:
            if self.data["is_sell"]:
                return -(self.data["quantity"] - self.instance.quantity)
            return self.instance.quantity

        if self.data["is_sell"]:
            return -self.data["quantity"]
        return 0


class MarketOrderManager(OrderManager):
    model = MarketOrder

    def update(self):
        with transaction.atomic():
            self.change_portfolio_quantity(self.instance.portfolio)

            self.instance.quantity = self.data["quantity"]
            self.instance.is_sell = self.data["is_sell"]
            self.instance.status = self.data["status"]
            self.instance.save()

            return self.instance


class LimitOrderManager(OrderManager):
    model = LimitOrder

    def update(self):
        with transaction.atomic():
            self.change_portfolio_quantity(self.instance.portfolio)

            self.instance.quantity = self.data["quantity"]
            self.instance.is_sell = self.data["is_sell"]
            self.instance.status = self.data["status"]
            self.instance.price = self.data["price"]
            self.instance.activated_status = self.data["activated_status"]
            self.instance.save()

            return self.instance
