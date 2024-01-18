from brokers.factories import InvestmentFactory
from django.test import TestCase
from faker import Faker
from tests.utils import TestUser
from users.factories import UserFactory


class UserViewSetTest(TestCase):
    def setUp(self) -> None:
        self.list_path = "/v1/users/"
        self.register_path = self.list_path + "register/"
        self.login_path = self.list_path + "login/"
        self.fake = Faker()
        self.new_user = UserFactory
        self.test_user = TestUser()

    # TODO: create list user negative using permissions
    def test_list_user_ok(self):
        _ = self.new_user()
        token = self.test_user.get_admin_token()

        response = self.client.get(
            self.list_path, headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertIsInstance(response.data[0], dict)
        self.assertNotIn("password", response.data[0])

    def test_list_user_permission_denied(self):
        _ = self.new_user()
        token = self.test_user.get_user_token()

        response = self.client.get(
            self.list_path, headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(response.status_code, 403)

    def test_create_user_ok(self):
        token = self.test_user.get_admin_token()

        response = self.client.post(
            path=self.register_path,
            data={
                "email": self.fake.email(),
                "username": self.fake.user_name(),
                "password": self.fake.password(),
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertNotIn("password", response.data)

    def test_create_user_with_duplicated_email(self):
        user = self.new_user()
        token = self.test_user.get_admin_token()

        response = self.client.post(
            path=self.register_path,
            data={
                "email": user.email,
                "username": self.fake.user_name(),
                "password": self.fake.password(),
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 400)

    def test_retrieve_user_ok(self):
        user = self.new_user()
        token = self.test_user.get_admin_token()
        path = f"{self.list_path}{user.pk}/"

        response = self.client.get(path, headers={"Authorization": f"Bearer {token}"})

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], user.id)
        self.assertNotIn("password", response.data)

    def test_retrieve_user_permission_denied(self):
        user = self.new_user()
        token = self.test_user.get_user_token()
        path = f"{self.list_path}{user.pk}/"

        response = self.client.get(path, headers={"Authorization": f"Bearer {token}"})

        self.assertEqual(response.status_code, 403)

    def test_update_user_ok(self):
        user = self.new_user()
        token = self.test_user.get_admin_token()
        subscriptions = [
            InvestmentFactory().id,
            InvestmentFactory().id,
            InvestmentFactory().id,
        ]

        is_blocked = True
        balance = f"{self.fake.pyint():.2f}"
        path = f"{self.list_path}{user.pk}/"

        response = self.client.put(
            path=path,
            data={
                "is_blocked": is_blocked,
                "balance": balance,
                "subscriptions": subscriptions,
            },
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], user.id)
        self.assertEqual(response.data["is_blocked"], is_blocked)
        self.assertEqual(response.data["balance"], balance)
        self.assertNotIn("password", response.data)

    def test_update_user_with_negative_balance(self):
        user = self.new_user()
        balance = f"{-self.fake.pyint():.2f}"
        token = self.test_user.get_admin_token()
        path = f"{self.list_path}{user.pk}/"

        response = self.client.put(
            path=path,
            data={
                "balance": balance,
            },
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 400)
