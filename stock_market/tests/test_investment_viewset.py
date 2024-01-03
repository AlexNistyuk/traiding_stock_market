from brokers.factories import InvestmentFactory
from brokers.models import InvestmentTypes
from django.test import TestCase
from faker import Faker
from tests.utils import TestUser


class InvestmentViewSetTest(TestCase):
    def setUp(self) -> None:
        self.path = "/v1/investments/"
        self.fake = Faker()
        self.new_investment = InvestmentFactory
        self.test_user = TestUser()

    def test_list_investment_ok(self):
        _ = self.new_investment()
        token = self.test_user.get_admin_token()

        response = self.client.get(
            self.path, headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertIsInstance(response.data[0], dict)

    def test_create_investment_ok(self):
        token = self.test_user.get_admin_token()

        response = self.client.post(
            path=self.path,
            data={
                "name": self.fake.name(),
                "price": self.fake.pyint(),
                "type": self.fake.random_choices(elements=InvestmentTypes.choices)[0][
                    0
                ],
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)

    def test_create_investment_with_duplicated_name(self):
        investment = self.new_investment()
        token = self.test_user.get_admin_token()

        response = self.client.post(
            path=self.path,
            data={
                "name": investment.name,
                "price": self.fake.pyint(),
                "type": self.fake.random_choices(elements=InvestmentTypes.choices)[0][
                    0
                ],
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 400)

    def test_retrieve_investment_ok(self):
        investment = self.new_investment()
        path = f"{self.path}{investment.id}/"
        token = self.test_user.get_admin_token()

        response = self.client.get(path, headers={"Authorization": f"Bearer {token}"})

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], investment.id)

    def test_update_investment_ok(self):
        investment = self.new_investment()
        path = f"{self.path}{investment.id}/"
        token = self.test_user.get_admin_token()

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
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], investment.id)

    def test_update_investment_permission_denied(self):
        investment = self.new_investment()
        path = f"{self.path}{investment.id}/"
        token = self.test_user.get_user_token()

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
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 403)

    def test_update_investment_with_negative_price(self):
        investment = self.new_investment()
        path = f"{self.path}{investment.id}/"
        token = self.test_user.get_admin_token()

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
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 400)

    def test_update_investment_with_incorrect_type(self):
        investment = self.new_investment()
        path = f"{self.path}{investment.id}/"
        token = self.test_user.get_admin_token()

        response = self.client.put(
            path=path,
            data={
                "name": self.fake.name(),
                "price": -self.fake.pyint(),
                "quantity": self.fake.pyint(),
                "type": self.fake.name(),
            },
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 400)
