from rest_framework import permissions, exceptions
from rest_framework import authentication
from models import Device
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import logging
logger = logging.getLogger(__name__)


class IsOwnerPermission(permissions.BasePermission):

    def has_permission(self, request, view, obj=None):
        if request.method == 'OPTIONS':
            return True
        if request.user is None:
            return False
        if 'username' in view.kwargs:
            return request.user.username == view.kwargs['username']
        return True

    def has_object_permission(self, request, view, obj):
        if request.user is None:
            return False
        if isinstance(obj, User) and obj == request.user:
            return True
        return obj.owner == request.user


class DeviceAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):

        auth = authentication.get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'device':
            msg = _('No authorization provided.')
            raise exceptions.NotAuthenticated(msg)
        if len(auth) == 1:
            msg = _('Invalid device header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid device header. Device string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)
        try:
            device_id = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid device header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)
        try:
            device = Device.objects.get(unique_device_id=device_id)
        except Device.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid device id.'))

        return (device.owner, device)
