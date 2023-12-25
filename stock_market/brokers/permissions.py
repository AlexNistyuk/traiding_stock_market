from rest_framework.permissions import BasePermission


class IsBuyerOrSeller(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.jwt_user.id in (obj.seller.owner_id, obj.buyer.owner_id)


class IsOrderOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.jwt_user.id == obj.portfolio.owner_id
