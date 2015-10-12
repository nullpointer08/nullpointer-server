"""hisra_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from hisra_models import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # GET /api/user/:username/media
    # POST /api/user/:username/media
    url(r'^api/user/(?P<username>[a-zA-Z0-9]*)/media$',
        views.MediaList.as_view()),

    # GET /api/user/:username/media/:id
    # DELETE /api/user/:username/media/:id
    url(r'^api/user/(?P<username>[a-zA-Z0-9]*)/media/(?P<id>[0-9]*)$',
        views.MediaDetail.as_view()),

    # GET /api/user/:username/playlist
    # POST /api/user/:username/playlist
    url(r'^api/user/(?P<username>[a-zA-Z0-9]*)/playlist$',
        views.UserPlaylistList.as_view()),

    # GET /api/user/:username/playlist/:id
    # PUT /api/user/:username/playlist/:id
    url(r'^api/user/(?P<username>[a-zA-Z0-9]*)/playlist/(?P<id>[0-9]*)$',
        views.UserPlaylistDetail.as_view()),

    # GET /api/device/:deviceid/playlist
    # PUT /api/device/:deviceid/playlist
    url(r'^api/device/(?P<deviceid>[a-zA-Z0-9]*)/playlist$',
        views.DevicePlaylistDetail.as_view()),

    # GET /api/user/:username/device
    url(r'^api/user/(?P<username>[a-zA-Z0-9]*)/device$',
        views.DeviceList.as_view()),

    # GET /api/user/:username/device/:id
    url(r'^api/user/(?P<username>[a-zA-Z0-9]*)/device/(?P<id>[a-zA-Z0-9_]*)$',
        views.DeviceDetail.as_view()),

    # POST /api/user
    url(r'^api/user$', views.UserList.as_view()),

    # GET /api/user/:username
    url(r'^api/user/(?P<username>[a-zA-Z0-9]*)$', views.UserDetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
