from django.db import IntegrityError
from django.test import TestCase
from faker import Faker
from users.factories import UserFactory
from users.models import Roles, User


class UserModelTest(TestCase):
    def setUp(self) -> None:
        self.fake = Faker()
        self.new_user = UserFactory
        self.user_count = lambda: User.objects.count()

    def test_create_user_ok(self):
        user_count = self.user_count()

        user = self.new_user()

        self.assertEqual(user_count + 1, self.user_count())
        self.assertIsInstance(user, User)

    def test_create_user_with_different_roles(self):
        user_count = self.user_count()

        user = User.objects.create_user(
            email=self.fake.email(),
            username=self.fake.user_name(),
            password=self.fake.password(),
        )
        admin = User.objects.create_superuser(
            email=self.fake.email(),
            username=self.fake.user_name(),
            password=self.fake.password(),
        )
        analyst = User.objects.create_analyst(
            email=self.fake.email(),
            username=self.fake.user_name(),
            password=self.fake.password(),
        )

        self.assertEqual(user_count + 3, self.user_count())
        self.assertEqual(user.role, Roles.USER)
        self.assertEqual(admin.role, Roles.ADMIN)
        self.assertEqual(analyst.role, Roles.ANALYST)

    def test_update_user_with_duplicated_email(self):
        user_count = self.user_count()

        user_1 = self.new_user()
        user_2 = self.new_user()

        user_2.email = user_1.email

        self.assertEqual(user_count + 2, self.user_count())
        self.assertRaises(IntegrityError, user_2.save)

    def test_update_user_with_duplicated_username(self):
        user_count = self.user_count()

        user_1 = self.new_user()
        user_2 = self.new_user()

        user_2.username = user_1.username

        self.assertEqual(user_count + 2, self.user_count())
        self.assertRaises(IntegrityError, user_2.save)

    def test_update_user_with_negative_balance(self):
        user_count = self.user_count()

        user_1 = self.new_user()

        user_1.balance = -self.fake.pyint()

        self.assertEqual(user_count + 1, self.user_count())
        self.assertRaises(IntegrityError, user_1.save)

    def test_user_representation(self):
        user_count = self.user_count()

        user = self.new_user()

        self.assertEqual(user_count + 1, self.user_count())
        self.assertEqual(str(user), user.username)
