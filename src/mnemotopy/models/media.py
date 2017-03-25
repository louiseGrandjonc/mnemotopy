import os

from django.db import models
from django.template.defaultfilters import slugify, truncatechars
from django.utils import timezone as datetime
from django.utils.crypto import get_random_string
from django.utils.html import escape
from django.utils.six import with_metaclass

from django_countries.fields import CountryField

from linguist.metaclasses import ModelMeta as LinguistMeta

from separatedvaluesfield.models import SeparatedValuesField

from .project import Project
from .geo import City


def get_filename(filename):
    fname, ext = os.path.splitext(filename)

    return unicode('%s.%s%s' % (slugify(truncatechars(fname, 50)), get_random_string(), escape(ext)))


def get_image_path(instance, filename):
    return os.path.join(instance.project.get_media_path(), 'image', get_filename(filename))


def get_video_path(instance, filename):
    return os.path.join(instance.project.get_media_path(), 'video', get_filename(filename))


def get_audio_path(instance, filename):
    return os.path.join(instance.project.get_media_path(), 'audio', get_filename(filename))


class BaseMedia(with_metaclass(LinguistMeta, models.Model)):
    title = models.CharField(max_length=255, null=True)
    project = models.ForeignKey(Project, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    realized_at = models.DateTimeField(null=True)
    country = CountryField(null=True)
    city = models.ForeignKey(City, null=True)
    position = models.PositiveIntegerField(null=True)

    class Meta:
        abstract = True


class Image(BaseMedia):
    image = models.ImageField(upload_to=get_image_path,
                              blank=True,
                              null=True)

    class Meta:
        abstract = False
        db_table = 'mnemotopy_project_image'
        linguist = {
            'identifier': 'image',
            'fields': ('title',)
        }


class Video(BaseMedia):
    url = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to=get_video_path, null=True, blank=True)
    languages = SeparatedValuesField(max_length=255,
                                     blank=True,
                                     null=True)

    class Meta:
        abstract = False
        db_table = 'mnemotopy_project_video'
        linguist = {
            'identifier': 'video',
            'fields': ('title',)
        }


class Audio(BaseMedia):
    url = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to=get_audio_path, null=True, blank=True)
    languages = SeparatedValuesField(max_length=255,
                                     blank=True,
                                     null=True)

    class Meta:
        abstract = False
        db_table = 'mnemotopy_project_audio'
        linguist = {
            'identifier': 'audio',
            'fields': ('title',)
        }
