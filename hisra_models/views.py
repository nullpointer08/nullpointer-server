from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from hisra_models.models import Media, Playlist, Device
from hisra_models.serializers import UserSerializer, MediaSerializer
from hisra_models.serializers import PlaylistSerializer, DeviceSerializer
from rest_framework import status
from django.contrib.auth.models import User


class MediaList(APIView):

    def get(self, request, username):
        '''
        GET /api/user/:username/media
        Returns all media belonging to the user
        '''
        # TODO: authentication
        media = Media.objects.all().filter(owner=username)
        serializer = MediaSerializer(media, many=True)
        return Response(serializer.data)

    def post(self, request, username):
        '''
        POST /api/user/:username/media
        Creates a new media for the user
        '''
        # TODO: authentication
        serializer = MediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=username)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MediaDetail(APIView):

    def get(self, request, username, id):
        '''
        GET /api/user/:username/media/:id
        Returns the media with the given id
        '''
        # TODO: authentication
        try:
            media = Media.objects.get(pk=id)
        except Media.DoesNotExist:
            return HttpResponse(status=404)

        serializer = MediaSerializer(media)
        return Response(serializer.data)

    def delete(self, request, username, id):
        '''
        DELETE /api/user/:username/media/:id
        Deletes an existing media
        '''
        # TODO: authentication
        try:
            media = Media.objects.get(pk=id)
        except Media.DoesNotExist:
            return HttpResponse(status=404)
        media.delete()
        return Response(status=200)


class UserPlaylistList(APIView):

    def get(self, request, username):
        '''
        GET /api/user/:username/playlist
        Returns all the playlists of the user
        '''
        # TODO: authentication
        playlists = Playlist.objects.all().filter(owner=username)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)

    def post(self, request, username):
        '''
        POST /api/user/:username/playlist
        Creates a new playlist for the user
        '''
        # TODO: authentication
        serializer = MediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=username)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UserPlaylistDetail(APIView):

    def get(self, request, username, id):
        '''
        GET /api/user/:username/playlist/:id
        Returns the playlist with the given id
        '''
        # TODO: authentication
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
        # TODO: authentication
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

    def get(self, request, username):
        '''
        GET /api/user/:username/device
        Returns all devices owned by the user
        '''
        # TODO: authentication
        devices = Device.objects.all().filter(owner=username)
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)

    def post(self, request, username):
        '''
        POST /api/user/:username/device
        Adds a device for the user
        '''
        # TODO: authentication
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
        serializer = DeviceSerializer(device, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):

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
