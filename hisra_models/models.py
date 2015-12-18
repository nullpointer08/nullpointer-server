from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from magic import from_file
from mimetypes import guess_type
import os

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MediaManager(models.Manager):

    @staticmethod
    def create_media(uploaded_file, user):
        old_file_path = uploaded_file.file.path
        filename = uploaded_file.filename
        new_file_path = os.path.join(os.path.dirname(old_file_path), filename)

        if os.path.isfile(new_file_path):
            filename = uploaded_file.upload_id + uploaded_file.filename
            new_file_path = os.path.join(os.path.dirname(old_file_path), filename)

        print "New file path %s" % new_file_path
        os.rename(old_file_path, new_file_path)
        media = Media(owner=user, media_file=new_file_path, md5=uploaded_file.md5)
        media.media_type = Media.determine_media_type(new_file_path)
        media.url = os.path.join(settings.MEDIA_URL, str(media.id))
        media.name = uploaded_file.filename
        media.save()
        return media


class Media(models.Model):
    VIDEO = 'V'
    IMAGE = 'I'
    WEB_PAGE = 'W'
    MEDIA_CHOICES = (
        ('V', 'video'),
        ('I', 'image'),
        ('W', 'web_page'),
    )

    owner = models.ForeignKey(User)
    media_file = models.CharField(max_length=256, blank=True)
    md5 = models.CharField(max_length=32, blank=True)
    url = models.CharField(max_length=256, blank=True)
    media_type = models.CharField(max_length=1, choices=MEDIA_CHOICES)
    name = models.CharField(max_length=256, blank=True)
    description = models.CharField(max_length=256, blank=True)

    objects = MediaManager()

    @staticmethod
    def is_supported_media_type(filename):
        file_type = guess_type(filename, strict=True)
        if not file_type:
            return False
        file_type = file_type[0].split('/',1)[0]
        logger.debug("TYPE: %s", file_type)
        if file_type in Media.MEDIA_CHOICES:
            return True
        return False

    @staticmethod
    def determine_media_type(file_path):
        mime = from_file(file_path, mime=True)
        file_type = mime.split('/', 1)[0]
        media_type = None
        for choice in Media.MEDIA_CHOICES:
            if choice[1] == file_type:
                media_type = choice[0]
        if not media_type or len(media_type) > 1:
            raise TypeError("media type error: ", file_type)
        return media_type

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
