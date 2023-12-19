from django.db.utils import IntegrityError
from django.test import TestCase
from faker import Faker
from users.factories import UserFactory
from users.models import Roles, User

fake = Faker()


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email=fake.email(),
            username=fake.user_name(),
            password=fake.password(),
        )
        admin = User.objects.create_superuser(
            email=fake.email(),
            username=fake.user_name(),
            password=fake.password(),
        )
        analyst = User.objects.create_analyst(
            email=fake.email(),
            username=fake.user_name(),
            password=fake.password(),
        )

        self.assertEqual(user.role, Roles.USER)
        self.assertEqual(admin.role, Roles.ADMIN)
        self.assertEqual(analyst.role, Roles.ANALYST)

    def test_equal_email(self):
        user_1 = UserFactory()
        user_2 = UserFactory()

        user_2.email = user_1.email

        self.assertRaises(IntegrityError, user_2.save)

    def test_equal_username(self):
        user_1 = UserFactory()
        user_2 = UserFactory()

        user_2.username = user_1.username

        self.assertRaises(IntegrityError, user_2.save)

    def test_balance(self):
        user = UserFactory()

        user.balance = -fake.pyint()

        self.assertRaises(IntegrityError, user.save)


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

    def test_create_user(self):
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

    def test_retrieve_user(self):
        user = UserFactory()

        response = self.client.get(f"{self.path}{user.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], user.id)
        self.assertNotIn("password", response.data)

    def test_update_user(self):
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
