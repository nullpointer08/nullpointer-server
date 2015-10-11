# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unique_device_id', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=256)),
                ('mediatype', models.CharField(max_length=1, choices=[(b'V', b'video'), (b'P', b'picture'), (b'W', b'web_page')])),
                ('name', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=256)),
                ('md5_checksum', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=256)),
                ('media_schedule_json', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('password_hash', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='playlist',
            name='owner',
            field=models.ForeignKey(to='hisra_models.User'),
        ),
        migrations.AddField(
            model_name='media',
            name='owner',
            field=models.ForeignKey(to='hisra_models.User'),
        ),
        migrations.AddField(
            model_name='device',
            name='owner',
            field=models.ForeignKey(to='hisra_models.User', null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='playlist',
            field=models.ForeignKey(default=None, blank=True, to='hisra_models.Playlist', null=True),
        ),
    ]
