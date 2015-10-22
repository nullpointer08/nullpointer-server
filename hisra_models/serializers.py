from rest_framework import serializers
from hisra_models.models import Media, Playlist, Device
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class MediaSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.id')
    md5_checksum = serializers.ReadOnlyField(source='file.md5')

    class Meta:
        model = Media
        fields = ('id', 'owner', 'url', 'mediatype', 'name', 'description',
                  'md5_checksum')


class PlaylistSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Playlist
        fields = ('id', 'owner', 'name', 'description', 'media_schedule_json')


class DeviceSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Device
        fields = ('unique_device_id', 'playlist', 'owner')
