from brokers.factories import InvestmentPortfolioFactory
from django.test import TestCase
from faker import Faker


class InvestmentPortfolioViewSetTest(TestCase):
    def setUp(self) -> None:
        self.path = "/v1/portfolios/"
        self.fake = Faker()
        self.new_porfolio = InvestmentPortfolioFactory

    # TODO: create list portfolio negative using permissions
    def test_list_portfolio_ok(self):
        _ = self.new_porfolio()

        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertIsInstance(response.data[0], dict)

    # TODO: create test create portfolio
    # TODO: create retrieve negative using permissions
    def test_retrieve_portfolio_ok(self):
        portfolio = self.new_porfolio()
        path = f"{self.path}{portfolio.id}/"

        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], portfolio.id)

    def test_update_portfolio_ok(self):
        portfolio = self.new_porfolio()
        path = f"{self.path}{portfolio.id}/"

        response = self.client.put(
            path=path,
            data={
                "count": self.fake.pyint(),
                "owner": portfolio.owner.id,
                "investment": portfolio.investment.id,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], portfolio.id)

    def test_update_portfolio_with_negative_count(self):
        portfolio = self.new_porfolio()
        path = f"{self.path}{portfolio.id}/"

        response = self.client.put(
            path=path,
            data={
                "count": -self.fake.pyint(),
                "owner": portfolio.owner.id,
                "investment": portfolio.investment.id,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
