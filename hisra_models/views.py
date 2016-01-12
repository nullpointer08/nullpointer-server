import json
import logging
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chunked_upload.exceptions import ChunkedUploadError
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from .models import Media, Playlist, Device
from .permissions import IsOwnerPermission, DeviceAuthentication
from .serializers import PlaylistSerializer, DeviceSerializer, UserSerializer, MediaSerializer, DeviceStatusSerializer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MediaDownloadView(APIView):

    authentication_classes = (TokenAuthentication, DeviceAuthentication)

    permission_classes = (IsOwnerPermission,)

    def get(self, request, media_id=None, owner_id=None, filename=None):
        if media_id:
            media = get_object_or_404(Media, pk=media_id)
        else:
            media = get_object_or_404(Media, owner_id=request.user.id, name=filename)

        self.check_object_permissions(request,media)

        response = HttpResponse()
        filename_str = os.path.join(str(media.owner.id), media.name)

        redirect_url = "/protected/{0}".format(filename_str)

        response['Content-Disposition'] = 'attachment; filename=%s' % media.name
        response['Content-Type'] = ''
        if media.md5:
            response['Content-MD5'] = media.md5

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
            logger.debug("Media saved")
        except Exception, e:
            logger.debug('Exception creating media: {0}'.format(e.message))
            raise ChunkedUploadError(status=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Creating media on server failed')

    def get_response_data(self, chunked_upload, request):
        return {'message': ("You successfully uploaded '%s' (%s bytes)!" %
                            (chunked_upload.filename, chunked_upload.offset))}


class MediaList(generics.ListCreateAPIView):
    serializer_class = MediaSerializer
    permission_classes = (IsOwnerPermission,)

    def get_queryset(self):
        return Media.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MediaDetail(generics.RetrieveDestroyAPIView):
    serializer_class = MediaSerializer
    permission_classes = (IsOwnerPermission,)

    def get_queryset(self):
        return Media.objects.filter(owner=self.request.user)

    def perform_destroy(self, instance):
        owner = instance.owner
        playlists = Playlist.objects.filter(owner=owner.id)
        for playlist in playlists:
            self.remove_media_from_playlist(instance, playlist)
        return super(MediaDetail, self).perform_destroy(instance)

    def remove_media_from_playlist(self, media, db_playlist):
        media_schedule = json.loads(db_playlist.media_schedule_json)
        new_schedule = []
        for item in media_schedule:
            if 'id' in item and item['id'] == media.id:
                continue
            new_schedule.append(item)
        media_schedule_json = json.dumps(new_schedule)
        db_playlist.media_schedule_json = media_schedule_json
        db_playlist.save()


class PlaylistList(generics.ListCreateAPIView):
    permission_classes = (IsOwnerPermission,)
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PlaylistDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlaylistSerializer
    permission_classes = (IsOwnerPermission,)

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)


class DeviceList(generics.ListAPIView):
    serializer_class = DeviceSerializer
    permission_classes = (IsOwnerPermission,)

    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)
    # Devices added and removed in Django admin for now


class DeviceDetail(generics.RetrieveUpdateAPIView):
    serializer_class = DeviceSerializer
    permission_classes = (IsOwnerPermission,)

    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)


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


class DeviceConfirmedPlaylist(APIView):
    authentication_classes = (DeviceAuthentication,)
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        if 'confirmed_playlist' not in request.data:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data='confirmed_playlist missing'
            )
        try:
            pl = Playlist.objects.get(pk=request.data['confirmed_playlist'])
        except Playlist.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data='Provided playlist does not exist'
            )
        device = request.auth
        print pl
        device.confirmed_playlist = pl
        device.save()
        return Response(status=status.HTTP_200_OK)

class StatusList(APIView):
    authentication_classes =  (DeviceAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        db_events = []
        for event in request.data:
            if self.is_valid(event):
                db_events.append(self.convert_to_db_form(event, request))
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = DeviceStatusSerializer(data=db_events, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def is_valid(self, event):
        fields = ('type', 'category', 'description', 'time', 'device_id')
        for field in fields:
            if field not in event:
                return False
        return True

    def convert_to_db_form(self, event, request):
        db_event = event
        type_int = 0
        type_str = db_event['type']
        if type_str == 'success':
            type_int = 1
        elif type_str == 'error':
            type_int = 0
        db_event['type'] = type_int
        db_event['device'] = request.auth.id
        del db_event['device_id']
        return db_event
