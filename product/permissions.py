from rest_framework import permissions

class CanMessageProduct(permissions.BasePermission):
    """
    Allows authenticated users to message a product.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated