from rest_framework.permissions import BasePermission
from .models import User
from rest_framework import permissions

class StaffPermission(BasePermission):

    # def has_object_permission(self, request, view, obj):
    #     return True

    def has_permission(self, request, view):
        return request.user.is_staff

class IsUpdateProfile(BasePermission):

    def has_permission(self, request, view):
        try:
            user_profile = User.objects.get(pk=view.kwargs['pk'])
        except:
            return False

        if request.user== user_profile:
            return True

        return False


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user