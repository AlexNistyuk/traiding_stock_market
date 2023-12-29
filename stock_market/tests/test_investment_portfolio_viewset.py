from brokers.factories import InvestmentFactory, InvestmentPortfolioFactory
from django.test import TestCase
from faker import Faker
from users.factories import UserFactory


class InvestmentPortfolioViewSetTest(TestCase):
    def setUp(self) -> None:
        self.path = "/v1/portfolios/"
        self.fake = Faker()
        self.new_portfolio = InvestmentPortfolioFactory

    # TODO: create list portfolio negative using permissions
    def test_list_portfolio_ok(self):
        _ = self.new_portfolio()

        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertIsInstance(response.data[0], dict)

    def test_create_portfolio_ok(self):
        owner = UserFactory()
        investment = InvestmentFactory()

        quantity = self.fake.pyint()

        response = self.client.post(
            path=self.path,
            data={
                "quantity": quantity,
                "owner": owner.id,
                "investment": investment.id,
            },
        )

        spend_amount = f"{investment.price * quantity:.2f}"

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["spend_amount"], spend_amount)

    def test_create_portfolio_with_negative_quantity(self):
        owner = UserFactory()
        investment = InvestmentFactory()

        response = self.client.post(
            path=self.path,
            data={
                "quantity": -self.fake.pyint(),
                "owner": owner.id,
                "investment": investment.id,
            },
        )

        self.assertEqual(response.status_code, 400)

    # TODO: create retrieve negative using permissions
    def test_retrieve_portfolio_ok(self):
        portfolio = self.new_portfolio()
        path = f"{self.path}{portfolio.id}/"

        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], portfolio.id)

    def test_update_portfolio_ok(self):
        portfolio = self.new_portfolio()
        path = f"{self.path}{portfolio.id}/"

        response = self.client.put(
            path=path,
            data={
                "quantity": portfolio.quantity + 1,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], portfolio.id)

    def test_update_portfolio_with_negative_quantity(self):
        portfolio = self.new_portfolio()
        path = f"{self.path}{portfolio.id}/"

        response = self.client.put(
            path=path,
            data={
                "quantity": -self.fake.pyint(),
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_update_portfolio_quantity_ok(self):
        portfolio = self.new_portfolio()
        portfolio.spend_amount = 0
        portfolio.quantity = 0
        portfolio.save()

        path = f"{self.path}{portfolio.id}/"
        quantity = self.fake.pyint()

        response = self.client.put(
            path=path,
            data={
                "quantity": quantity,
            },
            content_type="application/json",
        )

        spend_amount = f"{quantity*portfolio.investment.price:.2f}"

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["spend_amount"], spend_amount)
