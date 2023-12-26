from brokers.factories import InvestmentPortfolioFactory, MarketOrderFactory
from brokers.models import OrderStatuses
from django.test import TestCase
from faker import Faker


class MarketOrderViewSetTest(TestCase):
    def setUp(self) -> None:
        self.path = "/v1/orders/market/"
        self.fake = Faker()
        self.new_order = MarketOrderFactory
        self.new_portfolio = InvestmentPortfolioFactory

    # TODO: create list order negative using permissions
    def test_list_order_ok(self):
        _ = self.new_order()

        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertIsInstance(response.data[0], dict)

    def test_create_order_ok(self):
        portfolio = self.new_portfolio()

        response = self.client.post(
            path=self.path,
            data={
                "quantity": portfolio.quantity,
                "portfolio": portfolio.id,
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertIsInstance(response.data, dict)

    def test_create_order_with_zero_quantity(self):
        portfolio = self.new_portfolio()

        response = self.client.post(
            path=self.path,
            data={
                "quantity": 0,
                "portfolio": portfolio.id,
            },
        )

        self.assertEqual(response.status_code, 400)

    # TODO: create retrieve order negative using permissions

    def test_retrieve_order_ok(self):
        order = self.new_order()
        path = f"{self.path}{order.id}/"

        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], order.id)

    def test_update_order_ok(self):
        order = self.new_order()
        path = f"{self.path}{order.id}/"

        response = self.client.put(
            path=path,
            data={
                "quantity": self.fake.pyint(),
                "status": self.fake.random_choices(elements=OrderStatuses.choices)[0][
                    0
                ],
                "portfolio": order.portfolio.id,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], order.id)

    def test_update_order_with_negative_quantity(self):
        order = self.new_order()
        path = f"{self.path}{order.id}/"

        response = self.client.put(
            path=path,
            data={
                "quantity": -self.fake.pyint(),
                "status": self.fake.random_choices(elements=OrderStatuses.choices)[0][
                    0
                ],
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_update_order_with_incorrect_status(self):
        order = self.new_order()
        path = f"{self.path}{order.id}/"

        response = self.client.put(
            path=path,
            data={
                "quantity": -self.fake.pyint(),
                "status": self.fake.name(),
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
