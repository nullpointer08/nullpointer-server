from rest_framework import permissions, status
from rest_framework.authentication import BasicAuthentication
from django.http import HttpResponse
import logging
logger = logging.getLogger(__name__)

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

#
# def checkBasicAuthentication(view, request, *args, **kwargs):
#     basicAuth = BasicAuthentication
#     if request.user.id is not None:
#         pass
#     try:
#         request.user = basicAuth.authenticate(request)
#
#     except Exception, e:
#         logger.warn('Authentication failed: %s',e)
#         return HttpResponse(status=status.HTTP_403_FORBIDDEN)
