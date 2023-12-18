from brokers.models import Investment
from django.test import TestCase
from faker import Faker
from rest_framework.test import APIClient
from users.models import Roles


class UserCreateAPIViewTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.fake = Faker()
        self.path = "/v1/users/"

    def test_create_user(self):
        response_1 = self.client.post(
            path=self.path,
            data={
                "email": self.fake.email(),
                "username": self.fake.user_name(),
                "password": self.fake.password(),
            },
        )

        response_2 = self.client.post(
            path=self.path,
            data={
                "email": self.fake.email(),
                "username": self.fake.user_name(),
                "password": self.fake.password(),
            },
        )

        self.assertEqual(response_1.status_code, 201)
        self.assertEqual(response_2.status_code, 201)

    def test_equal_emails(self):
        email = self.fake.email()

        response_1 = self.client.post(
            path=self.path,
            data={
                "email": email,
                "username": self.fake.user_name(),
                "password": self.fake.password(),
            },
        )
        response_2 = self.client.post(
            path=self.path,
            data={
                "email": email,
                "username": self.fake.user_name(),
                "password": self.fake.password(),
            },
        )

        self.assertEqual(response_1.status_code, 201)
        self.assertEqual(response_2.status_code, 400)

    def test_equal_usernames(self):
        username = self.fake.user_name()

        response_1 = self.client.post(
            path=self.path,
            data={
                "email": self.fake.email(),
                "username": username,
                "password": self.fake.password(),
            },
        )
        response_2 = self.client.post(
            path=self.path,
            data={
                "email": self.fake.email(),
                "username": username,
                "password": self.fake.password(),
            },
        )

        self.assertEqual(response_1.status_code, 201)
        self.assertEqual(response_2.status_code, 400)

    def test_sensitives(self):
        response = self.client.post(
            path=self.path,
            data={
                "email": self.fake.email(),
                "username": self.fake.user_name(),
                "password": self.fake.password(),
            },
        )

        self.assertNotIn("password", response.data)

    def test_response_data(self):
        email = self.fake.email()
        username = self.fake.user_name()

        response = self.client.post(
            path=self.path,
            data={
                "email": email,
                "username": username,
                "password": self.fake.password(),
            },
        )

        self.assertEqual(response.data["email"], email)
        self.assertEqual(response.data["username"], username)
        self.assertEqual(response.data["role"], Roles.USER)
        self.assertIsNone(response.data["image"])
        self.assertFalse(response.data["is_blocked"])
        self.assertEqual(response.data["balance"], "0.00")
        self.assertEqual(response.data["subscriptions"], [])


class UserRetrieveUpdateAPIViewTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.fake = Faker()
        self.email = self.fake.email()
        self.username = self.fake.user_name()
        self.investments = [
            Investment.objects.create(
                name=self.fake.name(), type="stock", price=self.fake.pyint()
            ).id,
            Investment.objects.create(
                name=self.fake.name(), type="stock", price=self.fake.pyint()
            ).id,
        ]
        response = self.client.post(
            "/v1/users/",
            data={
                "email": self.email,
                "username": self.username,
                "password": self.fake.password(),
            },
        )
        self.id = response.data["id"]
        self.path = f"/v1/users/{self.id}/"

    def test_retrieve_user(self):
        response = self.client.get(path=self.path)

        self.assertEqual(response.data["email"], self.email)
        self.assertEqual(response.data["username"], self.username)

    def test_balance(self):
        response_1 = self.client.put(
            path=self.path,
            data={
                "balance": -self.fake.pyint(),
            },
        )
        response_2 = self.client.put(
            path=self.path,
            data={
                "balance": self.fake.pyint(),
            },
        )

        self.assertEqual(response_1.status_code, 400)
        self.assertEqual(response_2.status_code, 200)

    def test_update_user(self):
        balance = f"{self.fake.pyint():.2f}"

        response = self.client.put(
            path=self.path,
            data={
                "is_blocked": True,
                "balance": balance,
                "email": self.fake.email(),
                "username": self.fake.user_name(),
                "subscriptions": self.investments,
            },
        )

        self.assertTrue(response.data["is_blocked"])
        self.assertEqual(response.data["id"], self.id)
        self.assertEqual(response.data["balance"], balance)
        self.assertEqual(response.data["email"], self.email)
        self.assertEqual(response.data["username"], self.username)
        self.assertEqual(response.data["subscriptions"], self.investments)
