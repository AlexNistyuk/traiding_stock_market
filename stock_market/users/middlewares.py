from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from users.models import User
from utils.token import Token

from stock_market.settings import HTTP_AUTH_KEYWORD


class JWTAuthMiddleware(MiddlewareMixin):
    anonymous_urls = {
        "login",
        "register",
        "refresh",
    }

    def process_request(self, request):
        path = request.path if request.path.endswith("/") else request.path + "/"
        if path.split("/")[1] == "admin":
            return

        if path.split("/")[3] not in self.anonymous_urls:
            return self.__get_user(request)

    @staticmethod
    def __get_user(request):
        http_response = JsonResponse(
            data={"detail": "Authentication error"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

        header_list = request.headers.get("Authorization", "").split()
        if len(header_list) != 2:
            return http_response

        if header_list[0] != HTTP_AUTH_KEYWORD:
            return http_response

        token = header_list[1]
        payload = Token.get_payload(token)
        if not payload:
            return http_response

        try:
            user = User.objects.get(pk=payload["id"])
        except User.DoesNotExist:
            return http_response

        if user.is_blocked:
            return http_response

        request.jwt_user = user
