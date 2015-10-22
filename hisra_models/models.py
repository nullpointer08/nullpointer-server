from django.db import models
from django.contrib.auth.models import User
from chunked_upload.models import ChunkedUpload
from hisra_server.settings import MEDIA_ROOT
import os
import logging
import magic

class HisraChunkedUpload(ChunkedUpload):
    pass
HisraChunkedUpload._meta.get_field('user').null = True

def upload_to(instance):
    return os.path.join(MEDIA_ROOT+instance.user.id)

def determineMediaType(file):
        mime = magic.from_file(file,mime=True)
        fileType = mime.split('/',1)[0]
        return fileType
        
class Media(models.Model):
    VIDEO = 'V'
    IMAGE = 'P'
    WEBPAGE = 'W'
    MEDIA_CHOICES = (
        (VIDEO, 'video'),
        (IMAGE, 'image'),
        (WEBPAGE, 'web_page'),
    )
    file = models.FileField(upload_to=upload_to);
    owner = models.ForeignKey(User)
    url = models.CharField(max_length=256)
    media_type = models.CharField(max_length=1, choices=MEDIA_CHOICES)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)

    def createMedia(self, uploaded_file, request):
        media_type = determineMediaType(uploaded_file)
        if media_type not in Media.MEDIA_CHOICES:
            raise TypeError(media_type)
        m = Media(file=uploaded_file, owner=User, media_type=media_type, name=request.name, description=request.description)
        m.save()
        
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
