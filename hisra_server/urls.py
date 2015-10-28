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
from hisra_models.views import HisraChunkedUploadView, HisraChunkedUploadCompleteView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # GET /api/user/:username/media
    # POST /api/user/:username/media
    url(r'^api/user/(?P<username>[a-zA-Z0-9_]+)/media/?$',
        views.MediaList.as_view()),

    # GET /api/user/:username/media/:pk
    # DELETE /api/user/:username/media/:pk
    url(r'^api/user/(?P<username>[a-zA-Z0-9_]*)/media/(?P<pk>[0-9]+)/?$',
        views.MediaDetail.as_view()),

    # GET /api/user/:username/playlist
    # POST /api/user/:username/playlist
    url(r'^api/user/(?P<username>[a-zA-Z0-9_]+)/playlist/?$',
        views.PlaylistList.as_view()),

    # GET /api/user/:username/playlist/:id
    # PUT /api/user/:username/playlist/:id
    url(r'^api/user/(?P<username>[a-zA-Z0-9_]*)/playlist/(?P<id>[0-9]+)/?$',
        views.PlaylistDetail.as_view()),

    # GET /api/user/:username/device
    url(r'^api/user/(?P<username>[a-zA-Z0-9_]+)/device/?$',
        views.DeviceList.as_view()),

    # GET /api/user/:username/device/:id
    url(r'^api/user/(?P<username>[a-zA-Z0-9_]+)/device/(?P<id>[a-zA-Z0-9_]+)/?$',
        views.DeviceDetail.as_view()),

    # POST /api/user
    url(r'^api/user/?$', views.UserList.as_view()),

    # GET /api/user/:username
    url(r'^api/user/(?P<username>[a-zA-Z0-9_]+)/?$', views.UserDetail.as_view()),

    # GET /api/device/:deviceid/playlist
    url(r'^api/device/(?P<id>[a-zA-Z0-9_]+)/playlist/?$',
        views.DevicePlaylist.as_view()),

    # LOGIN
    url(r'^login/?$', 'django.contrib.auth.views.login', {'template_name':'login.html'}),
    # LOGOUT
    url(r'^logout/?$', 'django.contrib.auth.views.logout', {'template_name':'logout.html'} ),

    # /uploadfile/

    url(r'^uploadfile/?$',
        views.ChunkedUploadDemo.as_view(),name='chunked_upload'),

    url(r'^api/chunked_upload/?$',
        HisraChunkedUploadView.as_view(), name='api_chunked_upload'),
    url(r'^api/chunked_upload_complete/?$',
        HisraChunkedUploadCompleteView.as_view(),
        name='api_chunked_upload_complete'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
