from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Custom permission to only allow admin users to access certain views.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff
    
class IsSelfOrAdmin(BasePermission):
    """
    Custom permission to only allow users to access their own data or allow admin users to access any user's data.
    """
    
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated
        )
    
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id or request.user.is_staff