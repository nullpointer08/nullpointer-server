from django.db import models
from django.contrib.auth.models import User
from chunked_upload.models import ChunkedUpload
from hisra_server.settings import MEDIA_ROOT, MEDIA_URL

from hisra_models.utils import determine_media_type, MEDIA_CHOICES
import os

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

import uuid

class MediaManager(models.Manager):

    def create_media(self, uploaded_file, user):
        old_file_path = uploaded_file.file.path
        filename = uploaded_file.filename
        new_file_path = os.path.join(os.path.dirname(old_file_path), filename)
        if(os.path.isfile(new_file_path)):
            filename = uploaded_file.upload_id + uploaded_file.filename
            new_file_path = os.path.join(os.path.dirname(old_file_path), filename)
        print "New file path %s" % new_file_path
        os.rename(old_file_path, new_file_path)
        media = Media(owner=user, media_file=new_file_path, md5=uploaded_file.md5)
        media.media_type = determine_media_type(new_file_path)
        media.url = os.path.join(MEDIA_URL, str(media.id))
        media.name = uploaded_file.filename
        media.save()
        return media


class Media(models.Model):
    owner = models.ForeignKey(User)
    media_file = models.CharField(max_length=256)
    md5 = models.CharField(max_length=32)
    url = models.CharField(max_length=256)
    media_type = models.CharField(max_length=1, choices=MEDIA_CHOICES)
    name = models.CharField(max_length=256, blank=True)
    description = models.CharField(max_length=256, blank=True)

    objects = MediaManager()

    def __unicode__(self):
        return 'Media:[' + str(self.id) + ']'


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
