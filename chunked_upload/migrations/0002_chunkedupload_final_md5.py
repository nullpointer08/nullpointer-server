# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chunked_upload', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chunkedupload',
            name='final_md5',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
    ]
