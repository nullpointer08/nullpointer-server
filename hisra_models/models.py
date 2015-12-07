from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from chunked_upload.models import ChunkedUpload
from hisra_server.settings import MEDIA_ROOT, MEDIA_URL

from hisra_models.utils import determine_media_type, MEDIA_CHOICES
import os

import magic
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class HisraChunkedUpload(ChunkedUpload):
    pass
HisraChunkedUpload._meta.get_field('user').null = True


class MediaManager(models.Manager):

    def create_media(self, uploaded_file, user):
        file_path = os.path.join(str(user.id), uploaded_file.name)
        logger.debug("file path %s", file_path)
        logger.debug("upload_file.name %s", uploaded_file.name)
        # try:
        #     media = Media.objects.get(owner=user,media_file=file_path)
        #     logger.debug("Old file")
        # except ObjectDoesNotExist:
        #     logger.debug("New file")
        media = Media(owner=user)
        media.media_file.save(name=uploaded_file.name, content=uploaded_file)
        uploaded_file.close()
        logger.debug("media_file saved")
        media.media_type = determine_media_type(os.path.join(MEDIA_ROOT, file_path))
        media.url = os.path.join(MEDIA_URL, str(media.id))
        media.save()
        return media


def get_upload_to(instance, filename):
    return str(instance.owner.id) + '/' + filename


class Media(models.Model):
    owner = models.ForeignKey(User)
    media_file = models.FileField(upload_to=get_upload_to, blank=True)
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
