# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-10 09:48
from __future__ import unicode_literals

from django.db import migrations, models
import mnemotopy.models.media


class Migration(migrations.Migration):

    dependencies = [
        ('mnemotopy', '0003_project_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='compressed_image',
            field=models.ImageField(blank=True, null=True, upload_to=mnemotopy.models.media.get_compressed_image_path),
        ),
    ]