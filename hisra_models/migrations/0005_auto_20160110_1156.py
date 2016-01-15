# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hisra_models', '0004_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='description',
            field=models.CharField(max_length=256, blank=True),
        ),
    ]
