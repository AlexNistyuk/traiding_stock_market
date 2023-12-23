import abc

from brokers.models import InvestmentPortfolio


class IManager(abc.ABC):
    def __init__(self, validated_data: dict):
        self.data = validated_data

    @abc.abstractmethod
    def create(self):
        ...

    @abc.abstractmethod
    def update(self, instance):
        ...


class InvestmentPortfolioManager(IManager):
    def create(self):
        self.data["spend_amount"] = self.data["investment"].price * self.data["count"]

        return InvestmentPortfolio.objects.create(**self.data)

    def update(self, instance: InvestmentPortfolio):
        ...

    def __update_spend_amount(self, instance: InvestmentPortfolio) -> None:
        count_difference = self.data["count"] - instance.count
        if count_difference > 0:
            instance.spend_amount = (
                instance.spend_amount + self.data["investment"].price * count_difference
            )
