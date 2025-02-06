from brokers.factories import InvestmentPortfolioFactory
from brokers.models import InvestmentPortfolio
from django.db import IntegrityError
from django.db.models import QuerySet
from django.test import TestCase
from faker import Faker


class InvestmentPortfolioModelTest(TestCase):
    def setUp(self) -> None:
        self.fake = Faker()
        self.new_portfolio = InvestmentPortfolioFactory
        self.portfolio_count = lambda: InvestmentPortfolio.objects.count()

    def test_create_portfolio_ok(self):
        portfolio_count = self.portfolio_count()

        portfolio = self.new_portfolio()

        self.assertEqual(portfolio_count + 1, self.portfolio_count())
        self.assertIsInstance(portfolio, InvestmentPortfolio)

    def test_update_portfolio_with_negative_spend_amount(self):
        portfolio_count = self.portfolio_count()

        portfolio = self.new_portfolio()

        portfolio.spend_amount = -self.fake.pyint()

        self.assertEqual(portfolio_count + 1, self.portfolio_count())
        self.assertRaises(IntegrityError, portfolio.save)

    def test_update_portfolio_with_negative_quantity(self):
        portfolio_count = self.portfolio_count()

        portfolio = self.new_portfolio()

        portfolio.quantity = -self.fake.pyint()

        self.assertEqual(portfolio_count + 1, self.portfolio_count())
        self.assertRaises(IntegrityError, portfolio.save)

    def test_portfolio_quantity_desc_ordering(self):
        portfolio_count = self.portfolio_count()

        portfolio_1 = self.new_portfolio()
        portfolio_2 = self.new_portfolio()

        portfolio_list = [portfolio_1, portfolio_2]

        max_item = max(portfolio_list, key=lambda x: x.quantity)
        min_item = min(portfolio_list, key=lambda x: x.quantity)

        result = InvestmentPortfolio.objects.all()

        self.assertEqual(portfolio_count + 2, self.portfolio_count())
        self.assertIsInstance(result, QuerySet)
        self.assertEqual(result[0], max_item)
        self.assertEqual(result[1], min_item)
