from django.utils.deprecation import MiddlewareMixin


class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ...
