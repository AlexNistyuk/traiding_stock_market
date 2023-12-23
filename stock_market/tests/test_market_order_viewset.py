from brokers.factories import InvestmentPortfolioFactory, MarketOrderFactory
from brokers.models import InvestmentPortfolio, OrderStatuses
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
                "is_sell": True,
                "portfolio": portfolio.id,
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertIsInstance(response.data, dict)

    def test_create_sell_order_portfolio_quantity(self):
        portfolio = self.new_portfolio()

        response = self.client.post(
            path=self.path,
            data={
                "quantity": portfolio.quantity,
                "is_sell": True,
                "portfolio": portfolio.id,
            },
        )

        updated_portfolio = InvestmentPortfolio.objects.get(pk=portfolio.pk)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(updated_portfolio.quantity, 0)

    def test_create_sell_order_with_incorrect_quantity(self):
        portfolio = self.new_portfolio()

        response = self.client.post(
            path=self.path,
            data={
                "quantity": portfolio.quantity + 1,
                "is_sell": True,
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
                "is_sell": False,
                "portfolio": order.portfolio.id,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], order.id)

    def test_update_order_with_negative_count(self):
        order = self.new_order()
        path = f"{self.path}{order.id}/"

        response = self.client.put(
            path=path,
            data={
                "quantity": -self.fake.pyint(),
                "status": self.fake.random_choices(elements=OrderStatuses.choices)[0][
                    0
                ],
                "is_sell": False,
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
                "is_sell": False,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_update_not_sell_order_to_sell_ok(self):
        order = self.new_order()
        order.is_sell = False
        order.save()

        path = f"{self.path}{order.id}/"

        response = self.client.put(
            path=path,
            data={
                "quantity": order.portfolio.quantity,
                "status": "active",
                "is_sell": True,
            },
            content_type="application/json",
        )

        updated_portfolio = InvestmentPortfolio.objects.get(pk=order.portfolio.pk)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["quantity"], order.portfolio.quantity)
        self.assertEqual(updated_portfolio.quantity, 0)

    def test_update_not_sell_order_to_sell_with_incorrect_quantity(self):
        order = self.new_order()
        order.is_sell = False
        order.save()

        path = f"{self.path}{order.id}/"

        response = self.client.put(
            path=path,
            data={
                "quantity": order.portfolio.quantity + 1,
                "status": "active",
                "is_sell": True,
            },
            content_type="application/json",
        )

        updated_portfolio = InvestmentPortfolio.objects.get(pk=order.portfolio.pk)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(updated_portfolio.quantity, order.portfolio.quantity)

    def test_update_sell_order_to_not_sell_ok(self):
        order = self.new_order()
        order.is_sell = True
        order.save()

        portfolio = InvestmentPortfolio.objects.get(pk=order.portfolio.pk)
        portfolio.quantity = 0
        portfolio.save()

        selled_quantity = order.quantity
        path = f"{self.path}{order.id}/"
        quantity = self.fake.pyint()

        response = self.client.put(
            path=path,
            data={
                "quantity": quantity,
                "status": "active",
                "is_sell": False,
            },
            content_type="application/json",
        )

        updated_portfolio = InvestmentPortfolio.objects.get(pk=order.portfolio.pk)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["quantity"], quantity)
        self.assertEqual(updated_portfolio.quantity, selled_quantity)

    def test_update_sell_order_ok(self):
        order = self.new_order()
        order.is_sell = True
        order.save()

        path = f"{self.path}{order.id}/"

        response = self.client.put(
            path=path,
            data={
                "quantity": order.quantity + order.portfolio.quantity,
                "status": "active",
                "is_sell": True,
            },
            content_type="application/json",
        )

        updated_portfolio = InvestmentPortfolio.objects.get(pk=order.portfolio.pk)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(updated_portfolio.quantity, 0)

    def test_update_sell_order_with_incorrect_quantity(self):
        order = self.new_order()
        order.is_sell = True
        order.save()

        path = f"{self.path}{order.id}/"

        response = self.client.put(
            path=path,
            data={
                "quantity": order.quantity + order.portfolio.quantity + 1,
                "status": "active",
                "is_sell": True,
            },
            content_type="application/json",
        )

        updated_portfolio = InvestmentPortfolio.objects.get(pk=order.portfolio.pk)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(updated_portfolio.quantity, order.portfolio.quantity)
