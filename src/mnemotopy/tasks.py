# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from celery.task import task


@task(name='mnemotopy_media.tasks.upload_to_vimeo')
def upload_to_vimeo(media_id):
    from mnemotopy.models import Media

    media = Media.objects.get(pk=media_id)
    media.upload_to_vimeo()


@task(name='mnemotopy_media.tasks.edit_vimeo_information')
def edit_vimeo_information(media_id, change_thumbnail=False):
    from mnemotopy.models import Media

    media = Media.objects.get(pk=media_id)
    media.edit_vimeo_information(change_thumbnail=change_thumbnail)


@task(name='mnemotopy_media.tasks.upload_compressed_image')
def upload_compressed_image(media_id):
    from mnemotopy.models import Media

    media = Media.objects.get(pk=media_id)
    media.upload_compressed_image_file()
