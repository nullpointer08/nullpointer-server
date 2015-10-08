from django.db import models

#class User(models.Model):
#    username = models.CharField(max_length=50)

class Media(models.Model):
    VIDEO = 'V'
    PICTURE = 'P'
    WEBPAGE = 'W'
    MEDIA_CHOICES = (
        (VIDEO, 'video'),
        (PICTURE, 'picture'),
        (WEBPAGE, 'web_page'),
    )
#    owner = models.ForeignKey(User)
    uri = models.CharField(max_length=255)
    mediatype = models.CharField(max_length=1,
                                 choices=MEDIA_CHOICES)

class RotationPair(models.Model):
    media = models.ManyToManyField(Media)
    rotationTime = models.IntegerField()

class Playlist(models.Model):
    name = models.CharField(max_length=255)
    rotation = models.ForeignKey(RotationPair)

class Device(models.Model):
#    owner = models.ForeignKey(User)
    media = models.ManyToManyField(Media)
    playlist = models.ManyToManyField(Playlist)


