# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import forum.models.resized_image_field


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', forum.models.resized_image_field.ResizableImageField(upload_to=forum.models.resized_image_field.GetName(b'upfiles/'))),
                ('upload_url', models.CharField(max_length=2048, null=True, blank=True)),
                ('nodes', models.ManyToManyField(to='forum.Node')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='node',
            old_name='image',
            new_name='main_image',
        ),
        migrations.RenameField(
            model_name='noderevision',            
            old_name='image',
            new_name='main_image',
        ),
    ]
