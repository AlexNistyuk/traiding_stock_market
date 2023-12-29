from brokers.factories import InvestmentFactory
from brokers.models import InvestmentTypes
from django.test import TestCase
from faker import Faker


class InvestmentViewSetTest(TestCase):
    def setUp(self) -> None:
        self.path = "/v1/investments/"
        self.fake = Faker()
        self.new_investment = InvestmentFactory

    # TODO: create list investment negative using permissions
    def test_list_investment_ok(self):
        _ = self.new_investment()

        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertIsInstance(response.data[0], dict)

    def test_create_investment_ok(self):
        response = self.client.post(
            path=self.path,
            data={
                "name": self.fake.name(),
                "price": self.fake.pyint(),
                "type": self.fake.random_choices(elements=InvestmentTypes.choices)[0][
                    0
                ],
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)

    def test_create_investment_with_duplicated_name(self):
        investment = self.new_investment()

        response = self.client.post(
            path=self.path,
            data={
                "name": investment.name,
                "price": self.fake.pyint(),
                "type": self.fake.random_choices(elements=InvestmentTypes.choices)[0][
                    0
                ],
            },
        )

        self.assertEqual(response.status_code, 400)

    # TODO: create retrieve negative using permissions
    def test_retrieve_investment_ok(self):
        investment = self.new_investment()
        path = f"{self.path}{investment.id}/"

        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], investment.id)

    def test_update_investment_ok(self):
        investment = self.new_investment()
        path = f"{self.path}{investment.id}/"

        response = self.client.put(
            path=path,
            data={
                "name": self.fake.name(),
                "price": self.fake.pyint(),
                "quantity": self.fake.pyint(),
                "type": self.fake.random_choices(elements=InvestmentTypes.choices)[0][
                    0
                ],
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], investment.id)

    def test_update_investment_with_negative_price(self):
        investment = self.new_investment()
        path = f"{self.path}{investment.id}/"

        response = self.client.put(
            path=path,
            data={
                "name": self.fake.name(),
                "price": -self.fake.pyint(),
                "quantity": self.fake.pyint(),
                "type": self.fake.random_choices(elements=InvestmentTypes.choices)[0][
                    0
                ],
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_update_investment_with_incorrect_type(self):
        investment = self.new_investment()
        path = f"{self.path}{investment.id}/"

        response = self.client.put(
            path=path,
            data={
                "name": self.fake.name(),
                "price": -self.fake.pyint(),
                "quantity": self.fake.pyint(),
                "type": self.fake.name(),
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
