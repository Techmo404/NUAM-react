from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Permite el acceso solo a usuarios con role='ADMIN'
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "ADMIN"


class IsEmployee(BasePermission):
    """
    Permite el acceso solo a usuarios con role='EMP'
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "EMP"
