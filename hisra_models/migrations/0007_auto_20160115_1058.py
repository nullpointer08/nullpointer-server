# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hisra_models', '0006_auto_20160110_1253'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField()),
                ('category', models.CharField(max_length=20)),
                ('time', models.DateTimeField()),
                ('description', models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='confirmed_playlist',
            field=models.ForeignKey(related_name='confirmed_playlist', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='hisra_models.Playlist', null=True),
        ),
        migrations.AddField(
            model_name='devicestatus',
            name='device',
            field=models.ForeignKey(to='hisra_models.Device'),
        ),
    ]
