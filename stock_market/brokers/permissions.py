from rest_framework.permissions import BasePermission

from stock_market.settings import KAFKA_USERNAME


class IsPortfolioOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.jwt_user.id == obj.portfolio.owner_id


class IsKafkaUser(BasePermission):
    def has_permission(self, request, view):
        return request.jwt_user.username == KAFKA_USERNAME
