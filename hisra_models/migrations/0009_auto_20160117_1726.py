# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hisra_models', '0008_auto_20160115_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='updated',
        ),
        migrations.AddField(
            model_name='device',
            name='confirmed_playlist_update_time',
            field=models.DateTimeField(default=None, null=True, blank=True),
        ),
    ]
