from rest_framework import permissions


class IsSuperuserOrOwner(permissions.BasePermission):
    # def has_permission(self, request, view):
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #     return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user == obj:
            return True
        return False
