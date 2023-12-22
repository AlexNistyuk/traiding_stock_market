from datetime import datetime, timedelta, timezone

from jwt import JWT
from jwt.exceptions import JWTDecodeError
from jwt.jwk import OctetJWK
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
        self.jwt = JWT()

    def get_access_token(self):
        access_token_payload = {
            "id": self.user.id,
            "username": self.user.username,
            "role": self.user.role,
            "type": "access_token",
            "exp": self.__get_expire_time(
                timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRES_IN)
            ),
        }

        return self.jwt.encode(access_token_payload, JWK, alg=JWT_ALGORITHM)

    def get_refresh_token(self) -> str:
        refresh_token_payload = {
            "id": self.user.id,
            "type": "refresh_token",
            "exp": self.__get_expire_time(timedelta(days=JWT_REFRESH_TOKEN_EXPIRES_IN)),
        }

        return self.jwt.encode(refresh_token_payload, JWK, alg=JWT_ALGORITHM)

    def get_tokens(self) -> dict:
        return {
            "access_token": self.get_access_token(),
            "refresh_token": self.get_refresh_token(),
        }

    def get_payload(self, token: str) -> dict:
        try:
            return self.jwt.decode(token, JWK, algorithms={JWT_ALGORITHM})
        except JWTDecodeError:
            return {}

    @staticmethod
    def __get_expire_time(delta: timedelta) -> int:
        return int(datetime.now(tz=timezone.utc).timestamp() + delta.seconds)


JWK = OctetJWK(JWT_SECRET_KEY.encode())
