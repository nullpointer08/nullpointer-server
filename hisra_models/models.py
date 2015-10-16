from django.db import models
from django.contrib.auth.models import User
from chunked_upload.models import ChunkedUpload

class HisraChunkedUpload(ChunkedUpload):
    pass
HisraChunkedUpload._meta.get_field('user').null = True

class Media(models.Model):
    VIDEO = 'V'
    PICTURE = 'P'
    WEBPAGE = 'W'
    MEDIA_CHOICES = (
        (VIDEO, 'video'),
        (PICTURE, 'picture'),
        (WEBPAGE, 'web_page'),
    )
    owner = models.ForeignKey(User)
    url = models.CharField(max_length=256)
    mediatype = models.CharField(max_length=1, choices=MEDIA_CHOICES)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    md5_checksum = models.CharField(max_length=32)

    def __unicode__(self):
        return 'Media:[' + str(self.name) + ']'


class Playlist(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    media_schedule_json = models.TextField()

    def __unicode__(self):
        return 'Playlist:[' + str(self.name) + ']'


class Device(models.Model):
    unique_device_id = models.CharField(primary_key=True, max_length=256,
                                        unique=True)
    owner = models.ForeignKey(User, null=True, blank=True, default=None)
    playlist = models.ForeignKey(Playlist, null=True, blank=True, default=None)

    def __unicode__(self):
        return 'Device:[' + str(self.unique_device_id) + ']'
