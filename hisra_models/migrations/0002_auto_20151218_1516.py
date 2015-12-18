# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hisra_models', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='md5',
            field=models.CharField(max_length=32, blank=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='media_file',
            field=models.CharField(max_length=256, blank=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='url',
            field=models.CharField(max_length=256, blank=True),
        ),
    ]
