from brokers.factories import InvestmentPortfolioFactory, TradeFactory
from django.test import TestCase
from faker import Faker
from tests.utils import TestUser


class TradeViewSetTest(TestCase):
    def setUp(self) -> None:
        self.path = "/v1/trades/"
        self.fake = Faker()
        self.new_trade = TradeFactory
        self.new_portfolio = InvestmentPortfolioFactory
        self.test_user = TestUser()

    def test_list_trade_ok(self):
        _ = self.new_trade()
        token = self.test_user.get_admin_token()

        response = self.client.get(
            self.path, headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertIsInstance(response.data[0], dict)

    def test_create_trade_ok(self):
        token = self.test_user.get_admin_token()

        response = self.client.post(
            path=self.path,
            data={
                "quantity": self.fake.pyint(),
                "portfolio": self.new_portfolio().id,
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertIn("investment", response.data)

    def test_create_trade_with_zero_quantity(self):
        token = self.test_user.get_admin_token()

        response = self.client.post(
            path=self.path,
            data={
                "quantity": 0,
                "portfolio": self.new_portfolio().id,
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 400)

    def test_retrieve_trade_ok(self):
        trade = self.new_trade()
        path = f"{self.path}{trade.id}/"
        token = self.test_user.get_admin_token()

        response = self.client.get(path, headers={"Authorization": f"Bearer {token}"})

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], trade.id)

    def test_update_trade_ok(self):
        trade = self.new_trade()
        path = f"{self.path}{trade.id}/"
        token = self.test_user.get_admin_token()

        response = self.client.put(
            path=path,
            data={
                "quantity": self.fake.pyint(),
                "portfolio": trade.portfolio.id,
            },
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], trade.id)

    def test_update_trade_with_zero_quantity(self):
        trade = self.new_trade()
        path = f"{self.path}{trade.id}/"
        token = self.test_user.get_admin_token()

        response = self.client.put(
            path=path,
            data={
                "quantity": 0,
                "portfolio": trade.portfolio.id,
            },
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 400)
