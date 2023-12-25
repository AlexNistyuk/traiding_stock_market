import abc

from brokers.models import InvestmentPortfolio, LimitOrder, MarketOrder, Trade
from django.db import IntegrityError, transaction
from users.models import User
from utils.exceptions import Http400


class IService(abc.ABC):
    def __init__(self, validated_data: dict, instance=None):
        self.data = validated_data
        self.instance = instance

    @abc.abstractmethod
    def create(self):
        ...

    @abc.abstractmethod
    def update(self):
        ...


class UserService(IService):
    def create(self):
        return User.objects.create_user(**self.data)

    def update(self):
        try:
            self.instance.is_blocked = self.data["is_blocked"]
            self.instance.balance = self.data["balance"]
            self.instance.subscriptions.set(self.data["subscriptions"])
            self.instance.save()

            return self.instance
        except KeyError as exc:
            raise Http400({"detail": [f"{exc} is not provided"]})

    def change_password(self, user):
        user.set_password(self.data["new_password"])
        user.save()

    def set_subscriptions(self, user):
        try:
            user.subscriptions.set(self.data["subscriptions"])
            user.save()
        except KeyError:
            raise Http400({"detail": "'subscriptions' is not provided"})


class InvestmentPortfolioService(IService):
    def create(self):
        self.data["spend_amount"] = (
            self.data["investment"].price * self.data["quantity"]
        )

        return InvestmentPortfolio.objects.create(**self.data)

    def update(self):
        count_difference = self.data["quantity"] - self.instance.quantity
        if count_difference > 0:
            self.instance.spend_amount += (
                self.instance.investment.price * count_difference
            )

        self.instance.quantity = self.data["quantity"]
        self.instance.save()

        return self.instance


class OrderService(IService):
    model = None

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
                {
                    "detail": [
                        "The portfolio does not have the required quantity to sell"
                    ]
                }
            )

    def get_quantity_difference(self) -> int:
        if "is_sell" not in self.data:
            raise Http400({"detail": ["'is_sell' is not provided"]})

        if self.instance is None:
            return -self.data["quantity"] if self.data["is_sell"] else 0

        if self.instance.is_sell:
            if self.data["is_sell"]:
                return -(self.data["quantity"] - self.instance.quantity)
            return self.instance.quantity

        if self.data["is_sell"]:
            return -self.data["quantity"]
        return 0


class MarketOrderService(OrderService):
    model = MarketOrder

    def update(self):
        with transaction.atomic():
            self.change_portfolio_quantity(self.instance.portfolio)

            self.instance.quantity = self.data["quantity"]
            self.instance.is_sell = self.data["is_sell"]
            self.instance.status = self.data["status"]
            self.instance.save()

            return self.instance


class LimitOrderService(OrderService):
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


class TradeService(IService):
    def create(self):
        self.__check_data()

        self.data["investment"] = self.data["buyer"].investment
        self.data["price"] = self.data["investment"].price

        return Trade.objects.create(**self.data)

    def update(self):
        self.__check_data()

        self.instance.quantity = self.data["quantity"]
        self.instance.seller = self.data["seller"]
        self.instance.buyer = self.data["buyer"]
        self.instance.investment = self.data["buyer"].investment
        self.instance.price = self.instance.investment.price
        self.instance.save()

        return self.instance

    def __check_data(self):
        self.__check_seller_equal_buyer()
        self.__check_equal_investments()

    def __check_seller_equal_buyer(self):
        if self.data["seller"] == self.data["buyer"]:
            raise Http400({"seller": "Seller and buyer must not be the same"})

    def __check_equal_investments(self):
        if self.data["seller"].investment != self.data["buyer"].investment:
            raise Http400(
                {"investment": ["Seller and buyer investments must be the same"]}
            )
