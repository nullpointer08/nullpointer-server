from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

import os

from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from chunked_upload.exceptions import ChunkedUploadError
from chunked_upload.constants import http_status

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from hisra_models.models import Media, Playlist, Device, HisraChunkedUpload
from hisra_models.permissions import IsOwnerPermission
from hisra_models.serializers import UserSerializer, MediaSerializer
from hisra_models.serializers import PlaylistSerializer, DeviceSerializer
from hisra_server.settings import MEDIA_ROOT, MEDIA_URL, BASE_DIR
from hisra_models.utils import determine_media_type_from_filename

# when we deploy we might need these but not for now
#from hisra_server.wsgi import application
#from xsendfile import XSendfileApplication
#DOCUMENT_SENDING_APP = XSendfileApplication(os.path.join(BASE_DIR,MEDIA_ROOT))

from django.utils.encoding import smart_str

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MediaDownloadView(APIView):
    authentication_classes = (BasicAuthentication, SessionAuthentication)

    def get(self, request, path):
        logger.debug('calling download_document')
        filename = path.split('/')
        user_id_from_path = int(filename[0])
        filename = filename[1]
        authorized = self.check_authorization(request, user_id_from_path)
        print 'IS %s AUTHORIZED: %s' % (request.user, authorized)
        if not authorized:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
        logger.debug("authorization ok!")
        path = os.path.join(MEDIA_ROOT, path)
        response = HttpResponse(content=FileWrapper(file(path)))
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)
        return response

    def check_authorization(self, request, user_id):
        if request.user.is_authenticated and request.user.id == user_id:
            return True
        query_params = request.GET
        if 'device_id' in query_params:
            device_id = query_params['device_id']
            try:
                device = Device.objects.get(pk=device_id)
            except Device.DoesNotExist:
                logger.debug('No such device: %s' % device_id)
                return False
            device_owner = User.objects.get(pk=device.owner.id)
            if device_owner.id == user_id:
                return True
        return False


# temporary for testing
class ChunkedUploadDemo(TemplateView):
    template_name = 'chunked_upload_demo.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ChunkedUploadDemo, self).dispatch(*args, **kwargs)


class HisraChunkedUploadView(APIView, ChunkedUploadView):
    model = HisraChunkedUpload
    field_name = 'the_file'
    authentication_classes = (BasicAuthentication, SessionAuthentication)

    # check_permissions is called from both super classes atm.
    def check_permissions(self, request):
    #     checkBasicAuthentication(self, request)
        logger.debug("HisraChunkeDUploadView check_permissions user: %s", request.user)

#        if request.user.id is None:
#            raise ChunkedUploadError(
#                status=http_status.HTTP_403_FORBIDDEN,
#                detail='Authentication credentials were not provided'
#            )

    # def validate(self, request):
    #     filename = request.FILES.get(self.field_name).name
    #     path = os.path.join(MEDIA_ROOT + str(request.user.id), '/', filename)
    #     logger.debug("PATH %s", path)
    #     if os.path.exists(path):
    #         return HttpResponse(status=status.HTTP_409_CONFLICT)
    #
    #     if filename is not None and determine_media_type_from_filename(filename):
    #         return HttpResponse(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


class HisraChunkedUploadCompleteView(APIView, ChunkedUploadCompleteView):
    model = HisraChunkedUpload
    authentication_classes = (BasicAuthentication, SessionAuthentication)

    def check_permissions(self, request):
        logger.debug("HisraChunkeDUploadCompleteView check_permissions user: %s", request.user)
        if request.user.id is None:
            raise ChunkedUploadError(
                status=http_status.HTTP_403_FORBIDDEN,
                detail='Authentication credentials were not provided'
            )

    def on_completion(self, uploaded_file, request):
        try:
            Media.objects.create_media(uploaded_file, request.user)
            logger.info("Media saved")
        except Exception, e:
            logger.error(e)

    def get_response_data(self, chunked_upload, request):
        return {'message': ("You successfully uploaded '%s' (%s bytes)!" %
                            (chunked_upload.filename, chunked_upload.offset))}


class MediaList(APIView):

    def get(self, request, username):
        '''
        GET /api/user/:username/media
        Returns all devices owned by the user
        '''
        owners = User.objects.all().filter(username=username)
        if len(owners) == 0:
            return Response(status=status.HTTP_403_FORBIDDEN)
        assert len(owners) == 1
        owner = owners[0]
        media = Media.objects.all().filter(owner=owner)
        serializer = MediaSerializer(media, many=True)
        return Response(serializer.data)

    def post(self, request, username):
        '''
        POST /api/user/:username/device
        Adds a device for the user
        '''
        owners = User.objects.all().filter(username=username)
        if len(owners) == 0:
            return Response(status=status.HTTP_403_FORBIDDEN)
        assert len(owners) == 1
        owner = owners[0]
        serializer = MediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=owner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MediaDetail(generics.RetrieveDestroyAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = (IsOwnerPermission,)


class PlaylistList(APIView):

        def get(self, request, username):
            '''
            GET /api/user/:username/media
            Returns all devices owned by the user
            '''
            owners = User.objects.all().filter(username=username)
            if len(owners) == 0:
                return Response(status=status.HTTP_403_FORBIDDEN)
            assert len(owners) == 1
            owner = owners[0]
            playlists = Playlist.objects.all().filter(owner=owner)
            serializer = PlaylistSerializer(playlists, many=True)
            return Response(serializer.data)

        def post(self, request, username):
            '''
            POST /api/user/:username/device
            Adds a device for the user
            '''
            owners = User.objects.all().filter(username=username)
            if len(owners) == 0:
                return Response(status=status.HTTP_403_FORBIDDEN)
            assert len(owners) == 1
            owner = owners[0]
            serializer = PlaylistSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=owner)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        if device.playlist is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            playlist = Playlist.objects.get(pk=device.playlist.id)
        except Playlist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            device_owner = User.objects.get(pk=device.owner.id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            playlist_owner = User.objects.get(pk=playlist.owner.id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if playlist_owner != device_owner:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data, status=status.HTTP_200_OK)
