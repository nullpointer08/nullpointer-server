import logging
import os
import json

from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic.base import TemplateView

from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from chunked_upload.exceptions import ChunkedUploadError
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from .models import Media, Playlist, Device
from .permissions import IsOwnerPermission, DeviceAuthentication
from .serializers import PlaylistSerializer, DeviceSerializer, UserSerializer, MediaSerializer
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MediaDownloadView(APIView):

    authentication_classes = (TokenAuthentication, DeviceAuthentication)

    permission_classes = (IsOwnerPermission,)

    def get(self, request, media_id=None, owner_id=None, filename=None):
        logger.debug("REQUEST USER: %s", request.user)

        logger.debug("MediaDownloadView GET: media_id: %s owner_id: %s filename: %s", media_id, owner_id, filename)
        try:
            if not media_id:
                media = Media.objects.get(owner=owner_id, name=filename)
            else:
                media = Media.objects.get(id=media_id)
        except Media.DoesNotExist, e:
            # TODO questionable if we should inform a file does not exist without authorization
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        # User requested another users file!
        logger.debug('User %s requested user %s\'s media', request.user.username, media.owner.username)
        if request.user.id != media.owner.id:
            logger.debug('User %s requested user %s\'s media', request.user.username, media.owner.username)
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)

        logger.debug("authorization ok!")
        response = HttpResponse()
        filename_str = os.path.join(str(media.owner.id), media.name)

        redirect_url = "/protected/{0}".format(filename_str)
        logger.debug("Redirect url: %s", redirect_url)
        response['Content-Disposition'] = 'attachment; filename=%s' % media.name
        response['Content-Type'] = ''
        #response['Accept-Ranges'] = 'bytes'
        if media.md5:
            response['Content-MD5'] = media.md5
        logger.debug("Content md5: %s", response['Content-MD5'])

        logger.debug("Headers: %s", response._headers)
        response['X-Accel-Redirect'] = redirect_url

        return response


class ApiViewAuthenticationMixin(object):
    @method_decorator(api_view(['POST']))
    @method_decorator(authentication_classes(TokenAuthentication))
    @method_decorator(permission_classes(IsAuthenticated,))
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ApiViewAuthenticationMixin, self).dispatch(*args, **kwargs)


class HisraChunkedUploadView(ApiViewAuthenticationMixin, ChunkedUploadView):

    def is_valid_chunked_upload_request(self, **attrs):
        user = attrs['user']
        filename = attrs['filename']
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, str(user.id), str(filename))):
            raise ChunkedUploadError(status=status.HTTP_409_CONFLICT, detail='File already exists on the server.')
        if not Media.is_supported_media_type(attrs['filename']):
            raise ChunkedUploadError(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                                     detail='This file type is not supported.')

    def is_valid_chunked_upload(self, request, chunked_upload):
        if request.user != chunked_upload.user:
            raise ChunkedUploadError(
                status=status.HTTP_403_FORBIDDEN,
                detail='Authentication credentials were not correct'
            )
        return super(HisraChunkedUploadView, self).is_valid_chunked_upload(request, chunked_upload)


class HisraChunkedUploadCompleteView(ApiViewAuthenticationMixin, ChunkedUploadCompleteView):
    def on_completion(self, chunked_upload, request):
        try:
            Media.objects.create_media(chunked_upload, request.user)
            logger.info("Media saved")
        except Exception, e:
            logger.debug('Exception creating media: {0}'.format(e.message))
            raise ChunkedUploadError(status=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Creating media on server failed')

    def get_response_data(self, chunked_upload, request):
        return {'message': ("You successfully uploaded '%s' (%s bytes)!" %
                            (chunked_upload.filename, chunked_upload.offset))}


class MediaList(generics.ListCreateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = (IsOwnerPermission,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MediaDetail(generics.RetrieveDestroyAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = (IsOwnerPermission,)

    def perform_destroy(self, instance):
        owner = instance.owner
        playlists = Playlist.objects.all().filter(owner=owner.id)
        for playlist in playlists:
            self.remove_media_from_playlist(instance, playlist)
        return super(MediaDetail, self).perform_destroy(instance)

    def remove_media_from_playlist(self, media, db_playlist):
        media_schedule = json.loads(db_playlist.media_schedule_json.replace("'", '"'))
        new_schedule = []
        for item in media_schedule:
            if 'id' in item and item['id'] == media.id:
                continue
            new_schedule.append(item)
        media_schedule_json = json.dumps(new_schedule).replace('"', '\'')
        db_playlist.media_schedule_json = media_schedule_json
        db_playlist.save()


class PlaylistList(generics.ListCreateAPIView):
    queryset = Playlist.objects.all()
    permission_classes = (IsOwnerPermission,)
    serializer_class = PlaylistSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PlaylistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = (IsOwnerPermission,)


class DeviceList(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (IsOwnerPermission,)

    # Devices added and removed in Django admin for now


class DeviceDetail(generics.RetrieveUpdateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (IsOwnerPermission,)


class UserDetail(generics.RetrieveUpdateAPIView):
    # User creation handled through django admin for now
    queryset = User.objects.all()
    permission_classes = (IsOwnerPermission,)
    serializer_class = UserSerializer
    lookup_field = 'username'


class DevicePlaylist(APIView):
    authentication_classes = (DeviceAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        GET /api/device/:id/playlist
        """
        device = request.auth
        if not device.playlist:
            return Response('No playlist found', status.HTTP_404_NOT_FOUND)
        serializer = PlaylistSerializer(device.playlist)
        return Response(serializer.data, status=status.HTTP_200_OK)
