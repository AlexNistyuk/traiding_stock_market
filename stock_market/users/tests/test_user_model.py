from django.db import IntegrityError
from django.test import TestCase
from faker import Faker
from users.factories import UserFactory
from users.models import Roles, User

fake = Faker()


class UserModelTest(TestCase):
    def test_create_user_ok(self):
        user = UserFactory()

        self.assertIsInstance(user, User)

    def test_create_user_with_different_roles(self):
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

    def test_create_user_with_duplicated_email(self):
        user_1 = UserFactory()
        user_2 = UserFactory()

        user_2.email = user_1.email

        self.assertRaises(IntegrityError, user_2.save)

    def test_create_user_with_duplicated_username(self):
        user_1 = UserFactory()
        user_2 = UserFactory()

        user_2.username = user_1.username

        self.assertRaises(IntegrityError, user_2.save)

    def test_create_user_with_negative_balance(self):
        user_1 = UserFactory()

        user_1.balance = -fake.pyint()

        self.assertRaises(IntegrityError, user_1.save)
