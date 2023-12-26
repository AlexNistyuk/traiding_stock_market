from rest_framework.permissions import BasePermission


class IsPortfolioOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.jwt_user.id == obj.portfolio.owner_id
