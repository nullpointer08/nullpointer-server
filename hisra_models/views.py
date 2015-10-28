from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from hisra_models.models import Media, Playlist, Device, HisraChunkedUpload
from hisra_models.serializers import UserSerializer, MediaSerializer
from hisra_models.serializers import PlaylistSerializer, DeviceSerializer
from rest_framework import status
from django.contrib.auth.models import User
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from django.views.generic.base import TemplateView
from rest_framework import generics
from permissions import IsOwnerPermission
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# temporary for testing
class ChunkedUploadDemo(TemplateView):
    template_name = 'chunked_upload_demo.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ChunkedUploadDemo, self).dispatch(*args, **kwargs)


class HisraChunkedUploadView(ChunkedUploadView):
    model = HisraChunkedUpload
    field_name = 'the_file'


class HisraChunkedUploadCompleteView(ChunkedUploadCompleteView):
    model = HisraChunkedUpload

    def on_completion(self, uploaded_file, request):
        try:
            Media.objects.create_media(uploaded_file, request.user)
            logger.info("Media saved")
        except Exception, e:
            logger.error(e)

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


class PlaylistList(generics.ListCreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = (IsOwnerPermission,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PlaylistDetail(APIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = (IsOwnerPermission,)

    def get(self, request, username, id):
        '''
        GET /api/user/:username/playlist/:id
        Returns the playlist with the given id
        '''
        try:
            playlist = Playlist.objects.get(pk=id)
        except Playlist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data)

    def put(self, request, username, id):
        '''
        PUT /api/user/:username/playlist/:id
        Updates an existing playlist for the user
        '''
        try:
            playlist = Playlist.objects.get(pk=id)
        except Playlist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PlaylistSerializer(playlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeviceList(APIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (IsOwnerPermission,)
    '''
    Provides GET and POST for new device.
    '''

    def get(self, request, username):
        '''
        GET /api/user/:username/device
        Returns all devices owned by the user
        '''
        owners = User.objects.all().filter(username=username)
        if len(owners) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        assert len(owners) == 1
        owner = owners[0]
        devices = Device.objects.all().filter(owner=owner)
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)

    def post(self, request, username):
        '''
        POST /api/user/:username/device
        Adds a device for the user
        '''
        owners = User.objects.all().filter(username=username)
        if len(owners) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        assert len(owners) == 1
        owner = owners[0]
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=owner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeviceDetail(APIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (IsOwnerPermission,)

    def get(self, request, username, id):
        '''
        GET /api/user/:username/device/:id
        Returns details of a device
        '''
        try:
            device = Device.objects.get(pk=id)
        except Device.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DeviceSerializer(device)
        return Response(serializer.data)

    def put(self, request, username, id):
        '''
        GET /api/user/:username/device/:id
        Updates the device playlist
        '''
        try:
            device = Device.objects.get(pk=id)
        except Device.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if 'unique_device_id' not in request.data:
            request.data['unique_device_id'] = id

        serializer = DeviceSerializer(device, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # TODO We should limit who can create users or make some registration form
    #permission_classes = (IsOwnerPermission,)

    def post(self, request):
        '''
        POST /api/user
        Creates an new user
        '''
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerPermission,)
    '''
    GET /api/user/:username
    Returns some details for the user
    '''

    def get(self, request, username):
        users = User.objects.all().filter(username=username)
        if len(users) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        assert len(users) == 1

        user = users[0]
        serializer = UserSerializer(user)
        return Response(serializer.data)


class DevicePlaylist(APIView):
    def get(self, request, id):
        try:
            device = Device.objects.get(pk=id)
        except Device.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            playlist = Playlist.objects.get(pk=device.playlist.id)
        except Playlist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data, status=status.HTTP_200_OK)
