# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hisra_models', '0002_auto_20160107_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='media_schedule_json',
            field=jsonfield.fields.JSONField(),
        ),
    ]
