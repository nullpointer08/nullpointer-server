from rest_framework import serializers
from hisra_models.models import Media, Playlist, Device
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class MediaSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.id')
    media_type = serializers.ReadOnlyField(source='media_type')

    class Meta:
        model = Media
        fields = ('id', 'owner', 'url', 'media_type')


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
