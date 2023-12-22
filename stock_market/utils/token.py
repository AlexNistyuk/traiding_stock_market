from datetime import datetime, timedelta, timezone

import jwt
from users.models import User

from stock_market.settings import (
    JWT_ACCESS_TOKEN_EXPIRES_IN,
    JWT_ALGORITHM,
    JWT_REFRESH_TOKEN_EXPIRES_IN,
    JWT_SECRET_KEY,
)


class Token:
    def __init__(self, user: User = None):
        self.user = user

    def get_access_token(self):
        access_token_payload = {
            "id": self.user.id,
            "type": "access_token",
            "exp": self.__get_expire_time(
                timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRES_IN)
            ),
        }

        return jwt.encode(access_token_payload, JWT_SECRET_KEY, JWT_ALGORITHM)

    def get_refresh_token(self) -> str:
        refresh_token_payload = {
            "id": self.user.id,
            "type": "refresh_token",
            "exp": self.__get_expire_time(timedelta(days=JWT_REFRESH_TOKEN_EXPIRES_IN)),
        }

        return jwt.encode(refresh_token_payload, JWT_SECRET_KEY, JWT_ALGORITHM)

    def get_tokens(self) -> dict:
        return {
            "access_token": self.get_access_token(),
            "refresh_token": self.get_refresh_token(),
        }

    @staticmethod
    def get_payload(token: str) -> dict:
        try:
            return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return {}

    @staticmethod
    def __get_expire_time(delta: timedelta) -> int:
        return int(datetime.now(tz=timezone.utc).timestamp() + delta.seconds)
