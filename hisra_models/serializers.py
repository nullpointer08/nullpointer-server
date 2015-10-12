from rest_framework import serializers
from hisra_models.models import Media, Playlist, Device
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('id', 'owner', 'url', 'mediatype', 'name', 'description',
                  'md5_checksum')


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('owner', 'name', 'description', 'media_schedule_json')


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('owner', 'unique_device_id', 'playlist')
