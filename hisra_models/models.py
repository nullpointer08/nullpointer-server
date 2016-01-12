from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from magic import from_file
from mimetypes import guess_type
from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework import serializers
import os
from urlparse import urljoin
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MediaManager(models.Manager):

    @staticmethod
    def create_media(chunked_upload, user):
        old_file_path = chunked_upload.file.path
        filename = chunked_upload.filename
        new_file_path = os.path.join(os.path.dirname(old_file_path), filename)

        if os.path.isfile(new_file_path):
            filename = chunked_upload.upload_id + chunked_upload.filename
            new_file_path = os.path.join(os.path.dirname(old_file_path), filename)

        print "New file path %s" % new_file_path
        os.rename(old_file_path, new_file_path)
        media = Media(owner=user, media_file=new_file_path, md5=chunked_upload.completed_md5)
        media.media_type = Media.determine_media_type(new_file_path)
        media.name = filename
        media.save()
        media.url = urljoin(settings.MEDIA_URL, str(media.id))
        media.save()
        return media


@receiver(post_delete)
def something_deleted(sender, instance, **kwargs):
    """
    For debugging deletes
    """
    logger.debug(sender)
    logger.debug(instance)


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

    @receiver(post_delete)
    def delete_file(sender, instance, **kwargs):
        if sender == Media:
            os.remove(instance.media_file)
            # if user has no more files remove dir as well.
            # os.rmdir only removes empty dirs
            try:
                os.rmdir(os.path.dirname(instance.media_file))
            except OSError as e:
                pass

    @staticmethod
    def is_supported_media_type(filename):
        logger.debug('Checking filename: %s', filename)
        file_type = guess_type(filename, strict=False)
        if not file_type:
            logger.debug('Not file_type')
            return False
        file_type = file_type[0]
        if not file_type:
            logger.debug('Not file_type 0: %s', file_type)
            return False
        file_type = file_type.split('/',1)[0]
        logger.debug("TYPE: %s", file_type)
        for choice in Media.MEDIA_CHOICES:
            if choice[1] == file_type:
                return True
        logger.debug('Not in media choices')
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

from jsonfield import JSONField
class Playlist(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256, blank=True)
    media_schedule_json = JSONField()

    def __unicode__(self):
        return 'Playlist:[' + str(self.name) + ']'


class Device(models.Model):
    unique_device_id = models.CharField(max_length=256,
                                        unique=True)
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(User, null=True, blank=True, default=None)
    playlist = models.ForeignKey(Playlist, null=True, blank=True, default=None)
    confirmed_playlist = models.ForeignKey(Playlist, related_name='confirmed_playlist', null=True, blank=True, default=None)

    def __unicode__(self):
        return 'Device:[' + str(self.unique_device_id) + ']'


class DeviceStatus(models.Model):
    device = models.ForeignKey(Device)
    type = models.IntegerField()
    category = models.CharField(max_length=20)
    time = models.DateTimeField()
    description = models.CharField(max_length=128)
