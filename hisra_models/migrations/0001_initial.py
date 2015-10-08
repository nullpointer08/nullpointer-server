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
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uri', models.CharField(max_length=255)),
                ('mediatype', models.CharField(max_length=1, choices=[(b'V', b'video'), (b'P', b'picture'), (b'W', b'web_page')])),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RotationPair',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rotationTime', models.IntegerField()),
                ('media', models.ManyToManyField(to='hisra_models.Media')),
            ],
        ),
        migrations.AddField(
            model_name='playlist',
            name='rotation',
            field=models.ForeignKey(to='hisra_models.RotationPair'),
        ),
        migrations.AddField(
            model_name='device',
            name='media',
            field=models.ManyToManyField(to='hisra_models.Media'),
        ),
        migrations.AddField(
            model_name='device',
            name='playlist',
            field=models.ManyToManyField(to='hisra_models.Playlist'),
        ),
    ]
