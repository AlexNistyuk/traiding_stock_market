from rest_framework.permissions import BasePermission
from users.models import Roles


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.jwt_user.role == Roles.ADMIN


class IsAnalyst(BasePermission):
    def has_permission(self, request, view):
        return request.jwt_user.role == Roles.ANALYST


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.jwt_user.role == Roles.USER

    def has_object_permission(self, request, view, obj):
        return request.jwt_user.pk == obj.pk


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner_id == request.jwt_user.id
