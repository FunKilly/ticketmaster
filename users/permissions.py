from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Allows access only to fact checkers.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user