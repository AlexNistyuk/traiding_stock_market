import abc

from brokers.models import InvestmentPortfolio, LimitOrder, MarketOrder, Trade
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
        self.instance.spend_amount += self.instance.investment.price * count_difference

        self.instance.quantity = self.data["quantity"]
        self.instance.save()

        return self.instance


class OrderService(IService):
    model = None

    def create(self):
        self.data["investment"] = self.data["portfolio"].investment

        return self.model.objects.create(**self.data)


class MarketOrderService(OrderService):
    model = MarketOrder

    def update(self):
        self.instance.quantity = self.data["quantity"]
        self.instance.status = self.data["status"]
        self.instance.save()

        return self.instance


class LimitOrderService(OrderService):
    model = LimitOrder

    def update(self):
        self.instance.quantity = self.data["quantity"]
        self.instance.status = self.data["status"]
        self.instance.price = self.data["price"]
        self.instance.activated_status = self.data["activated_status"]
        self.instance.save()

        return self.instance


class TradeService(IService):
    def create(self):
        self.data["investment"] = self.data["portfolio"].investment
        self.data["price"] = self.data["investment"].price

        return Trade.objects.create(**self.data)

    def update(self):
        self.instance.quantity = self.data["quantity"]
        self.instance.portfolio = self.data["portfolio"]
        self.instance.investment = self.data["portfolio"].investment
        self.instance.price = self.instance.investment.price
        self.instance.save()

        return self.instance
