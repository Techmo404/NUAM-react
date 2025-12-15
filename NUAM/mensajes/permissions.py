from rest_framework.permissions import BasePermission


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "EMP"


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "ADMIN"
