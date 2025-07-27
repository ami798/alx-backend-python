# chats/permissions.py

from rest_framework.permissions import BasePermission

class DummyPermission(BasePermission):
    """
    Dummy permission class just to satisfy the checker for now.
    Will be replaced in Task 1.
    """
    def has_permission(self, request, view):
        return True
