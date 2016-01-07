# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chunked_upload', '0002_chunkedupload_final_md5'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chunkedupload',
            old_name='final_md5',
            new_name='completed_md5',
        ),
    ]
