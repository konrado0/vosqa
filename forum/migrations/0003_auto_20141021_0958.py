# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import forum.models.resized_image_field


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20141017_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='height',
            field=models.PositiveIntegerField(null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='image',
            name='width',
            field=models.PositiveIntegerField(null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=forum.models.resized_image_field.ResizableImageField(height_field=b'height', width_field=b'width', upload_to=forum.models.resized_image_field.GetName(b'upfiles/')),
        ),        
    ]
