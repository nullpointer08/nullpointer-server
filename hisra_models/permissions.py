from rest_framework import permissions


class IsOwnerPermission(permissions.BasePermission):

    def has_permission(self, request, view, obj=None):
        if request.user is None:
            return False
        return request.user.username == view.kwargs['username']

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the snippet.
        if request.user is None:
            return False
        return obj.owner == request.user
