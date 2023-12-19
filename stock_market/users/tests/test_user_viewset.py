from django.test import TestCase
from faker import Faker
from users.factories import UserFactory

fake = Faker()


class UserViewSetTest(TestCase):
    def setUp(self) -> None:
        self.path = "/v1/users/"

    def test_list_user(self):
        _ = UserFactory()

        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertIsInstance(response.data[0], dict)
        self.assertNotIn("password", response.data[0])

    def test_create_user_ok(self):
        response = self.client.post(
            path=self.path,
            data={
                "email": fake.email(),
                "username": fake.user_name(),
                "password": fake.password(),
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertNotIn("password", response.data)

    def test_create_user_with_duplicated_email(self):
        user = UserFactory()
        response = self.client.post(
            path=self.path,
            data={
                "email": user.email,
                "username": fake.user_name(),
                "password": fake.password(),
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_retrieve_user(self):
        user = UserFactory()

        response = self.client.get(f"{self.path}{user.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], user.id)
        self.assertNotIn("password", response.data)

    def test_update_user_ok(self):
        user = UserFactory()

        is_blocked = True
        balance = f"{fake.pyint():.2f}"

        response = self.client.put(
            path=f"{self.path}{user.pk}/",
            data={
                "is_blocked": is_blocked,
                "balance": balance,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], user.id)
        self.assertEqual(response.data["is_blocked"], is_blocked)
        self.assertEqual(response.data["balance"], balance)
        self.assertNotIn("password", response.data)

    def test_update_user_with_negative_balance(self):
        user = UserFactory()
        balance = f"{-fake.pyint():.2f}"

        response = self.client.put(
            path=f"{self.path}{user.pk}/",
            data={
                "balance": balance,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
