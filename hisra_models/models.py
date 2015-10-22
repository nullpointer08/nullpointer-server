from django.db import models
from django.contrib.auth.models import User
from chunked_upload.models import ChunkedUpload
from hisra_server.settings import MEDIA_ROOT, MEDIA_URL
import os
import magic
import logging
logger = logging.getLogger('django')


class HisraChunkedUpload(ChunkedUpload):
    pass
HisraChunkedUpload._meta.get_field('user').null = True

def upload_to(instance):
    return os.path.join(MEDIA_ROOT+instance.user.id)

def determineMediaType(file):
    mime = magic.from_file(file,mime=True)
    fileType = mime.split('/',1)[0]
    return fileType


class MediaManager(models.Manager):
    def createMedia(self, uploaded_file, request, user):
        dir = os.path.join(MEDIA_ROOT,str(user.id))
        try:
            os.stat(dir)
        except Exception,e:
            os.makedirs(dir)
        file_path = os.path.join(dir,uploaded_file.name)
        with open(os.path.join(dir,uploaded_file.name), 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        destination.close()

        media_type = determineMediaType(str(destination.name))
        for choice in Media.MEDIA_CHOICES:
            if(choice[1] == media_type):
                media_type = choice[0]
        if len(media_type) > 1:
            raise TypeError(media_type)
        m = Media(owner=user, media_type=media_type, file=destination, url=os.path.join(MEDIA_URL,str(user.id),destination.name))
        return m

class Media(models.Model):
    VIDEO = 'V'
    IMAGE = 'P'
    WEBPAGE = 'W'
    MEDIA_CHOICES = (
        (VIDEO, 'video'),
        (IMAGE, 'image'),
        (WEBPAGE, 'web_page'),
    )
    #file = models.FileField(upload_to=upload_to, blank=True)
    owner = models.ForeignKey(User)
    url = models.CharField(max_length=256)
    media_type = models.CharField(max_length=1, choices=MEDIA_CHOICES)
    name = models.CharField(max_length=256, blank=True)
    description = models.CharField(max_length=256, blank=True)

    objects = MediaManager()

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
