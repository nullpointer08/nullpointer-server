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
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from chunked_upload.exceptions import ChunkedUploadError
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from .models import Media, Playlist, Device
from .permissions import IsOwnerPermission, DeviceAuthentication
from .serializers import PlaylistSerializer, DeviceSerializer, UserSerializer, MediaSerializer
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MediaDownloadView(APIView):

    authentication_classes = (BasicAuthentication, DeviceAuthentication)

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


# temporary for testing
class ChunkedUploadDemo(TemplateView):
    template_name = 'chunked_upload_demo.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ChunkedUploadDemo, self).dispatch(*args, **kwargs)


class ApiViewAuthenticationMixin(object):
    authentication_classes = (BasicAuthentication, SessionAuthentication)

    def authenticate(self, request):
        request = Request(request=request, authenticators=[auth() for auth in self.authentication_classes])
        if not request.user.is_authenticated:
            raise ChunkedUploadError(status=401, detail="Authorization required")


class HisraChunkedUploadView(ApiViewAuthenticationMixin, ChunkedUploadView):

    def check_permissions(self, request):
        self.authenticate(request)
        super(HisraChunkedUploadView,self).check_permissions(request)

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
    do_md5_check = False

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(HisraChunkedUploadCompleteView, self).dispatch(*args, **kwargs)

    def check_permissions(self, request):
        self.authenticate(request)

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


class MediaList(APIView):

    permission_classes = (IsOwnerPermission,)

    def get(self, request, username):
        """
        GET /api/user/:username/media
        Returns all media owned by the user
        """

        media = Media.objects.all().filter(owner=request.user)
        serializer = MediaSerializer(media, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, username):
        """
        POST /api/user/:username/media
        Adds a device for the user
        """
        serializer = MediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MediaDetail(generics.RetrieveDestroyAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = (IsOwnerPermission,)

    def perform_destroy(self, instance):
        owner = instance.owner
        playlists = Playlist.objects.all().filter(owner=owner.id)
        for playlist in playlists:
            self.remove_media_from_playlist(instance, playlist)
        if os.path.isfile(instance.media_file):
            os.remove(instance.media_file)
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



class PlaylistList(APIView):

    permission_classes = (IsOwnerPermission,)
    def get(self, request, username):
        """
        GET /api/user/:username/media
        Returns all devices owned by the user
        """
        playlists = Playlist.objects.all().filter(owner=request.user)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)

    def post(self, request, username):
        """
        POST /api/user/:username/device
        Adds a device for the user
        """
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaylistDetail(APIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    permission_classes = (IsOwnerPermission,)

    def get(self, request, username, id):
        """
        GET /api/user/:username/playlist/:id
        Returns the playlist with the given id
        """
        try:
            playlist = Playlist.objects.get(pk=id)
        except Playlist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data)

    def put(self, request, username, id):
        """
        PUT /api/user/:username/playlist/:id
        Updates an existing playlist for the user
        """
        try:
            playlist = Playlist.objects.get(pk=id)
        except Playlist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PlaylistSerializer(playlist, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username, id):
        """
        DELETE /api/user/:username/playlist/:id
        Deletes a playlist
        """
        try:
            playlist = Playlist.objects.get(pk=id)
        except Playlist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        playlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeviceList(APIView):
    """
    Provides GET and POST for new device.
    """

    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    permission_classes = (IsOwnerPermission,)

    def get(self, request, username):
        """
        GET /api/user/:username/device
        Returns all devices owned by the user
        """
        devices = Device.objects.all().filter(owner=request.user)
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)

    # Devices added and removed in Django admin for now


class DeviceDetail(APIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    permission_classes = (IsOwnerPermission,)

    def get(self, request, username, id):
        """
        GET /api/user/:username/device/:id
        Returns details of a device
        """
        try:
            device = Device.objects.get(pk=id)
        except Device.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DeviceSerializer(device)
        return Response(serializer.data)

    def put(self, request, username, id):
        """
        GET /api/user/:username/device/:id
        Updates the device playlist
        """
        if request.user.username != username:
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            device = Device.objects.get(pk=id)
        except Device.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        playlist_id = request.data['playlist']
        try:
            playlist = Playlist.objects.get(pk=playlist_id)
        except Playlist.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if playlist.owner.id != device.owner.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        request.data['unique_device_id'] = id

        serializer = DeviceSerializer(device, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User creation handled through django admin for now
'''
class UserList(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # TODO We should limit who can create users or make some registration form
    #permission_classes = (IsOwnerPermission,)

    def post(self, request):
        """
        POST /api/user
        Creates an new user
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''


class UserDetail(APIView):
    permission_classes = (IsOwnerPermission,)

    def get(self, request, username):
        """
        GET /api/user/:username
        Returns some details for the user
        """
        if request.user.username != username:
            return Response(status=status.HTTP_403_FORBIDDEN)

        user = User.objects.get(username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class DevicePlaylist(APIView):
    authentication_classes = (DeviceAuthentication,)

    def get(self, request):
        """
        GET /api/device/:id/playlist
        """
        device = request.auth
        if not device.playlist:
            return Response('No playlist found', status.HTTP_404_NOT_FOUND)
        serializer = PlaylistSerializer(request.auth.playlist)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthenticationView(APIView):

    def post(self, request):
        """
        POST /api/authentication
        """
        if request.user.is_authenticated:
            return Response({"success": True}, status=status.HTTP_200_OK)
        return Response(
            {"success": False},
            status=status.HTTP_401_UNAUTHORIZED
        )
