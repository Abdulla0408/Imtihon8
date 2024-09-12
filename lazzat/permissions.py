from rest_framework.permissions import BasePermission

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
         return request.user.is_authenticated and (request.user.is_staff or obj.staff.user == request.user)
