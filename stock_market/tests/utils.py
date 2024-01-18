from rest_framework.test import APIClient
from users.factories import UserFactory
from users.models import Roles
from utils.token import Token


class TestUser:
    def __init__(self):
        self.client = APIClient()
        self.login_endpoint = "/v1/users/login/"

    def get_user_token(self):
        user = UserFactory()
        user.role = Roles.USER
        user.save()

        return Token(user).get_access_token()

    def get_analyst_token(self):
        user = UserFactory()
        user.role = Roles.ANALYST
        user.save()

        return Token(user).get_access_token()

    def get_admin_token(self):
        user = UserFactory()
        user.role = Roles.ADMIN
        user.save()

        return Token(user).get_access_token()
