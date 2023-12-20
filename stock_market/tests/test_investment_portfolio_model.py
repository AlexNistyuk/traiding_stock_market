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

    def test_create_portfolio_ok(self):
        portfolio = self.new_portfolio()

        self.assertIsInstance(portfolio, InvestmentPortfolio)

    def test_update_portfolio_with_negative_spend_amount(self):
        portfolio = self.new_portfolio()

        portfolio.spend_amount = -self.fake.pyint()

        self.assertRaises(IntegrityError, portfolio.save)

    def test_update_portfolio_with_negative_count(self):
        portfolio = self.new_portfolio()

        portfolio.count = -self.fake.pyint()

        self.assertRaises(IntegrityError, portfolio.save)

    def test_portfolio_count_desc_ordering(self):
        portfolio_1 = self.new_portfolio()
        portfolio_2 = self.new_portfolio()

        portfolio_list = [portfolio_1, portfolio_2]

        max_item = max(portfolio_list, key=lambda x: x.count)
        min_item = min(portfolio_list, key=lambda x: x.count)

        result = InvestmentPortfolio.objects.all()

        self.assertIsInstance(result, QuerySet)
        self.assertEqual(result[0], max_item)
        self.assertEqual(result[1], min_item)
