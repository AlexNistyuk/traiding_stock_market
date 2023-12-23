import factory
from brokers.models import (
    Investment,
    InvestmentPortfolio,
    InvestmentTypes,
    LimitOrder,
    MarketOrder,
    OrderActivatedStatuses,
    OrderStatuses,
    Recommendation,
    Trade,
)
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from users.factories import UserFactory


class FuzzyTextChoice(FuzzyChoice):
    def fuzz(self):
        return super().fuzz()[0]


class InvestmentFactory(DjangoModelFactory):
    name = factory.Faker("name")
    image = factory.django.ImageField(filename="test.png")
    price = factory.Faker("pyint")
    quantity = factory.Faker("pyint")
    type = FuzzyTextChoice(choices=InvestmentTypes.choices)

    class Meta:
        model = Investment


class InvestmentPortfolioFactory(DjangoModelFactory):
    quantity = factory.Faker("pyint")
    spend_amount = factory.Faker("pyint")
    owner = factory.SubFactory(UserFactory)
    investment = factory.SubFactory(InvestmentFactory)

    class Meta:
        model = InvestmentPortfolio


class OrderFactory(DjangoModelFactory):
    quantity = factory.Faker("pyint")
    is_sell = factory.Faker("boolean")
    status = FuzzyTextChoice(choices=OrderStatuses.choices)
    portfolio = factory.SubFactory(InvestmentPortfolioFactory)
    investment = factory.SubFactory(InvestmentFactory)


class MarketOrderFactory(OrderFactory):
    class Meta:
        model = MarketOrder


class LimitOrderFactory(OrderFactory):
    price = factory.Faker("pyint")
    activated_status = FuzzyTextChoice(choices=OrderActivatedStatuses.choices)

    class Meta:
        model = LimitOrder


class TradeFactory(DjangoModelFactory):
    quantity = factory.Faker("pyint")
    price = factory.Faker("pyint")
    seller = factory.SubFactory(InvestmentPortfolioFactory)
    buyer = factory.SubFactory(InvestmentPortfolioFactory)
    investment = factory.SubFactory(InvestmentFactory)

    class Meta:
        model = Trade


class RecommendationFactory(DjangoModelFactory):
    counter = factory.Faker("pyint")
    investment = factory.SubFactory(InvestmentFactory)

    class Meta:
        model = Recommendation
