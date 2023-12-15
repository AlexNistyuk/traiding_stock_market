from unittest import TestCase

from faker import Faker
from rest_framework.test import APIClient


class InvestmentListCreateAPIViewTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.fake = Faker()
        self.path = "/api/investments/"

    def test_create_investment(self):
        response = self.client.post(
            path=self.path,
            data={
                "name": self.fake.name(),
                "price": "12.12",
                "type": "stock",
            },
        )

        self.assertEqual(response.status_code, 201)

    def test_equal_names(self):
        name = self.fake.name()

        response_1 = self.client.post(
            path=self.path,
            data={
                "name": name,
                "price": "12.12",
                "type": "stock",
            },
        )
        response_2 = self.client.post(
            path=self.path,
            data={
                "name": name,
                "price": "12.12",
                "type": "stock",
            },
        )

        self.assertEqual(response_1.status_code, 201)
        self.assertEqual(response_2.status_code, 400)

    def test_price(self):
        response_1 = self.client.post(
            path=self.path,
            data={
                "name": self.fake.name(),
                "price": "-12.12",
                "type": "stock",
            },
        )
        response_2 = self.client.post(
            path=self.path,
            data={
                "name": self.fake.name(),
                "price": "12.12",
                "type": "stock",
            },
        )

        self.assertEqual(response_1.status_code, 400)
        self.assertEqual(response_2.status_code, 201)

    def test_count(self):
        response_1 = self.client.post(
            path=self.path,
            data={
                "name": self.fake.name(),
                "price": "12.12",
                "type": "stock",
                "count": "12",
            },
        )
        response_2 = self.client.post(
            path=self.path,
            data={
                "name": self.fake.name(),
                "price": "12.12",
                "type": "cryptocurrency",
                "count": "-12",
            },
        )

        self.assertEqual(response_1.status_code, 201)
        self.assertEqual(response_2.status_code, 400)

    def test_list_investments(self):
        response = self.client.get(self.path)

        self.assertIsInstance(response.data, list)
        self.assertIsInstance(response.data[0], dict)


class InvestmentRetrieveUpdateAPIViewTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.fake = Faker()
        self.name = self.fake.name()
        self.type = "stock"
        response = self.client.post(
            path="/api/investments/",
            data={
                "name": self.name,
                "price": self.fake.pyint(),
                "type": self.type,
            },
        )
        self.id = response.data["id"]
        self.path = f"/api/investments/{self.id}/"

    def test_retrieve_investment(self):
        response = self.client.get(path=self.path)

        self.assertEqual(response.data["name"], self.name)

    def test_update_investment(self):
        name = self.fake.name()
        count = self.fake.pyint()
        price = self.fake.pyint()
        inv_type = "cryptocurrency"

        response = self.client.put(
            path=self.path,
            data={
                "name": name,
                "count": count,
                "price": price,
                "type": inv_type,
            },
        )

        self.assertEqual(response.data["id"], self.id)
        self.assertEqual(response.data["name"], name)
        self.assertEqual(response.data["count"], count)
        self.assertEqual(response.data["price"], f"{price:.2f}")
        self.assertEqual(response.data["type"], inv_type)
        self.assertNotEqual(response.data["created_at"], response.data["updated_at"])
