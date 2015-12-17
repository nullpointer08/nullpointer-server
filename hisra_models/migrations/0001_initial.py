# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('unique_device_id', models.CharField(max_length=256, unique=True, serialize=False, primary_key=True)),
                ('owner', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('media_file', models.CharField(max_length=256)),
                ('md5', models.CharField(max_length=32)),
                ('url', models.CharField(max_length=256)),
                ('media_type', models.CharField(max_length=1, choices=[(b'V', b'video'), (b'I', b'image'), (b'W', b'web_page')])),
                ('name', models.CharField(max_length=256, blank=True)),
                ('description', models.CharField(max_length=256, blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=256)),
                ('media_schedule_json', models.TextField()),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='playlist',
            field=models.ForeignKey(default=None, blank=True, to='hisra_models.Playlist', null=True),
        ),
    ]
