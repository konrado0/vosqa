# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20141021_0958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='main_image',
        ),
        migrations.RemoveField(
            model_name='noderevision',
            name='main_image',
        ),
        migrations.AddField(
            model_name='node',
            name='main_image',
            field=models.ForeignKey(default=None, blank=True, to='forum.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='noderevision',
            name='main_image',
            field=models.ForeignKey(default=None, blank=True, to='forum.Image', null=True),
            preserve_default=True,
        ),
    ]
