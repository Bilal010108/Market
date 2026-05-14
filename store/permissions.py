from rest_framework.permissions import BasePermission


class IsSellerPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.user_role == 'seller')


class IsOwnerPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.user_role == 'owner')


class IsAdministratorPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.user_role == 'administrator')


class IsOwnerOrAdministrator(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.user_role in ('owner', 'administrator'))