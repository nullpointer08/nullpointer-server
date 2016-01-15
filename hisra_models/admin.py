from django.contrib import admin
from models import Media, Playlist, Device, DeviceStatus

# Register your models here.
admin.site.register(Media)
admin.site.register(Playlist)
admin.site.register(Device)
admin.site.register(DeviceStatus)