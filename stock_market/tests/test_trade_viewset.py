from brokers.factories import InvestmentPortfolioFactory, TradeFactory
from django.test import TestCase
from faker import Faker


class TradeViewSetTest(TestCase):
    def setUp(self) -> None:
        self.path = "/v1/trades/"
        self.fake = Faker()
        self.new_trade = TradeFactory
        self.new_portfolio = InvestmentPortfolioFactory

    # TODO: create list trade negative using permissions
    def test_list_trade_ok(self):
        _ = self.new_trade()

        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertIsInstance(response.data[0], dict)

    def test_create_trade_ok(self):
        response = self.client.post(
            path=self.path,
            data={
                "quantity": self.fake.pyint(),
                "portfolio": self.new_portfolio().id,
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertIn("investment", response.data)

    def test_create_trade_with_zero_quantity(self):
        response = self.client.post(
            path=self.path,
            data={
                "quantity": 0,
                "portfolio": self.new_portfolio().id,
            },
        )

        self.assertEqual(response.status_code, 400)

    # TODO: create retrieve trade negative using permissions
    def test_retrieve_trade_ok(self):
        trade = self.new_trade()
        path = f"{self.path}{trade.id}/"

        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], trade.id)

    def test_update_trade_ok(self):
        trade = self.new_trade()
        path = f"{self.path}{trade.id}/"

        response = self.client.put(
            path=path,
            data={
                "quantity": self.fake.pyint(),
                "portfolio": trade.portfolio.id,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], trade.id)

    def test_update_trade_with_zero_quantity(self):
        trade = self.new_trade()
        path = f"{self.path}{trade.id}/"

        response = self.client.put(
            path=path,
            data={
                "quantity": 0,
                "portfolio": trade.portfolio.id,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
