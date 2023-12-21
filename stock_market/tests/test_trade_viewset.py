from brokers.factories import TradeFactory
from django.test import TestCase
from faker import Faker


class TradeViewSetTest(TestCase):
    def setUp(self) -> None:
        self.path = "/v1/trades/"
        self.fake = Faker()
        self.new_trade = TradeFactory

    # TODO: create list trade negative using permissions
    def test_list_trade_ok(self):
        _ = self.new_trade()

        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertIsInstance(response.data[0], dict)

    # TODO: create create trade when creating logic will be written
    # TODO: create create trade negative when creating logic will be written
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
                "count": self.fake.pyint(),
                "seller": trade.seller.id,
                "buyer": trade.buyer.id,
                "investment": trade.investment.id,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], trade.id)

    def test_update_trade_with_negative_count(self):
        trade = self.new_trade()
        path = f"{self.path}{trade.id}/"

        response = self.client.put(
            path=path,
            data={
                "count": -self.fake.pyint(),
                "seller": trade.seller.id,
                "buyer": trade.buyer.id,
                "investment": trade.investment.id,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
