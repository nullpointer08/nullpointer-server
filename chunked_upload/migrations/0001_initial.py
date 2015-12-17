# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import chunked_upload.models
from django.conf import settings
import hisra_server.settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChunkedUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upload_id', models.CharField(default=chunked_upload.models.generate_upload_id, unique=True, max_length=32, editable=False)),
                ('file', models.FileField(max_length=255, upload_to=hisra_server.settings.generate_filename)),
                ('filename', models.CharField(max_length=255)),
                ('offset', models.BigIntegerField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.PositiveSmallIntegerField(default=1, choices=[(1, 'Uploading'), (2, 'Complete')])),
                ('completed_on', models.DateTimeField(null=True, blank=True)),
                ('user', models.ForeignKey(related_name='chunked_uploads', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
