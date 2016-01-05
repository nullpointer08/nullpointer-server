from rest_framework import serializers
from hisra_models.models import Media, Playlist, Device
from django.contrib.auth.models import User
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class MediaSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Media
        fields = ('id', 'owner', 'url', 'media_type', 'md5', 'name', 'description')


class PlaylistSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.id')
    playlist_url = serializers.SerializerMethodField()
    class Meta:
        model = Playlist
        fields = ('id', 'owner', 'playlist_url', 'name', 'description', 'media_schedule_json')

    def get_playlist_url(self, obj):
        return settings.MEDIA_URL


class DeviceSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Device
        fields = ('unique_device_id', 'playlist', 'owner')
