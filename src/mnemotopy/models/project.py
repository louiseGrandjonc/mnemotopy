from django.db import models
from django.utils import timezone as datetime
from django.utils.six import with_metaclass

from django_countries.fields import CountryField

from linguist.metaclasses import ModelMeta as LinguistMeta

from sluggable.fields import SluggableField

from .geo import City
from .category import Category
from .tag import Tag
from .slug import ProjectSlug


class Project(with_metaclass(LinguistMeta, models.Model)):
    slug = SluggableField(decider=ProjectSlug)
    name = models.CharField(max_length=255, null=True)
    subtitle = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(default=datetime.now)
    started_at = models.DateTimeField(null=True)
    ended_at = models.DateTimeField(null=True)
    country = CountryField(null=True)
    city = models.ForeignKey(City, null=True)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    archived = models.BooleanField(default=False)
    position = models.PositiveIntegerField(null=True)
    published = models.BooleanField(default=False)

    class Meta:
        db_table = 'mnemotopy_project'
        linguist = {
            'identifier': 'project',
            'fields': ('name', 'subtitle', 'description')
        }
