from rest_framework import serializers
from hisra_models.models import Media, Playlist, Device, DeviceStatus
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
    media_url = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ('id', 'owner', 'media_url', 'updated', 'name', 'description', 'media_schedule_json')

    def get_media_url(self, obj):
        return settings.MEDIA_URL


class DeviceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Device
        fields = ('name', 'playlist', 'owner', 'id', 'confirmed_playlist', 'confirmed_playlist_update_time')


class DeviceStatusSerializer(serializers.ModelSerializer):
    device_id = serializers.ReadOnlyField(source='device.id')
    device_name = serializers.ReadOnlyField(source='device.name')

    class Meta:
        model = DeviceStatus
        fields = ('id', 'device_id', 'device_name', 'type', 'category', 'description', 'time')
