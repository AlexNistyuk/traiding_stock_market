from brokers.factories import InvestmentFactory
from brokers.models import Investment
from django.db import IntegrityError
from django.test import TestCase
from faker import Faker


class InvestmentModelTest(TestCase):
    def setUp(self) -> None:
        self.fake = Faker()
        self.new_investment = InvestmentFactory

    def test_create_investment_ok(self):
        investment = self.new_investment()

        self.assertIsInstance(investment, Investment)

    def test_update_investment_with_duplicated_name(self):
        investment_1 = self.new_investment()
        investment_2 = self.new_investment()

        investment_2.name = investment_1.name

        self.assertRaises(IntegrityError, investment_2.save)

    def test_update_investment_with_negative_price(self):
        investment = self.new_investment()
        investment.price = -self.fake.pyint()

        self.assertRaises(IntegrityError, investment.save)

    def test_update_investment_with_negative_count(self):
        investment = self.new_investment()
        investment.count = -self.fake.pyint()

        self.assertRaises(IntegrityError, investment.save)

    def test_investment_representation(self):
        investment = self.new_investment()

        self.assertEqual(str(investment), investment.name)
