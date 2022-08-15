from rest_framework import permissions
from .models import User


class IsAdminPermission(permissions.BasePermission):
    """
    Global permission check for User is Admin or not.
    """
    message = "User is not admin."

    def has_permission(self, request, view):
        return request.user.is_admin


class IsNormalPermission(permissions.BasePermission):
    """
    Global permission check for User is Normal User or not.
    """
    message = "User is not normal user."

    def has_permission(self, request, view):
        return not request.user.is_admin
