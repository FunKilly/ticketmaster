from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Allows access only to fact checkers.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

    def has_permission(self, request, view):
        return all([request.user, request.user.is_authenticated])
