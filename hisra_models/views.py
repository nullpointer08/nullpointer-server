from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from hisra_models.models import Media, Playlist, User, Device
from hisra_models.serializers import MediaSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class MediaList(APIView):

    '''
    GET /api/user/:username/media
    Returns all media belonging to the user
    '''
    def get(self, request, username):
        # TODO: authentication
        media = Media.objects.all()
        serializer = MediaSerializer(media, many=True)

        return JSONResponse(serializer.data)

    '''
    POST /api/user/:username/media
    Creates a new media for the user
    '''
    def post(self, request, username):
        # TODO: authentication
        data = JSONParser().parse(request)
        serializer = MediaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


class MediaDetail(APIView):
    '''
    GET /api/user/:username/media/:id
    Returns the media with the given id
    '''
    def get(self, request, username, id):
        # TODO: authentication
        try:
            media = Media.objects.get(pk=id)
        except Media.DoesNotExist:
            return HttpResponse(status=404)

        serializer = MediaSerializer(media)
        return JSONResponse(serializer.data)

    '''
    DELETE /api/user/:username/media/:id
    Deletes an existing media
    '''
    def delete(self, request, username, id):
        # TODO: authentication
        try:
            media = Media.objects.get(pk=id)
        except Media.DoesNotExist:
            return HttpResponse(status=404)
        media.delete()
        return JSONResponse(status=200)


class UserPlaylistList(APIView):

    '''
    GET /api/user/:username/playlist
    Returns all the playlists of the user
    '''
    def get(self, request, username):
        pass

    '''
    POST /api/user/:username/playlist
    Creates a new playlist for the user
    '''
    def post(self, request, username):
        pass


class UserPlaylistDetail(APIView):

    '''
    GET /api/user/:username/playlist/:id
    Returns the playlist with the given id
    '''
    def get(self, request, username, id):
        pass

    '''
    PUT /api/user/:username/playlist/:id
    Updates an existing playlist for the user
    '''
    def put(self, request, username, id):
        pass


class DevicePlaylistDetail(APIView):

    '''
    GET /api/device/:deviceid/playlist
    Returns the playlist used by the given device
    '''
    def get(self, request, device_id):
        pass

    '''
    PUT /api/device/:deviceid/playlist
    Updates a playlist for the device
    '''
    def put(self, request, device_id):
        pass


class DeviceList(APIView):

    '''
    GET /api/user/:username/device
    Returns all devices owned by the user
    '''
    def get(self, request, username):
        pass


class DeviceDetail(APIView):

    '''
    POST /api/user/:username/device/:id
    Adds a device for the user
    '''
    def post(sefl, request, username, id):
        pass


class UserList(APIView):

    '''
    POST /api/user
    Creates an new user
    '''
    def post(self, request, username):
        pass


class UserDetail(APIView):

    '''
    GET /api/user/:username
    Returns some details for the user
    '''
    def get(self, request, username):
        pass

# Create your views here.
