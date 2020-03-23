from rest_framework.permissions import BasePermission


class StaffPermission(BasePermission):

    # def has_object_permission(self, request, view, obj):
    #     return True

    def has_permission(self, request, view):
        return request.user.is_staff
