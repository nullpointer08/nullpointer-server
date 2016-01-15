# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hisra_models', '0007_auto_20160115_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 15, 11, 58, 51, 239737, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playlist',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 15, 11, 58, 56, 998174, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
