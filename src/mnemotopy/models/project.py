from django.db import models
from django.utils import timezone as datetime
from django.utils.six import with_metaclass
from django.utils.translation import ugettext_lazy as _

from django_countries.fields import CountryField

from sluggable.fields import SluggableField

from .geo import City
from .category import Category
from .tag import Tag
from .slug import ProjectSlug


class Project(models.Model):
    slug = SluggableField(decider=ProjectSlug, null=False)
    name = models.CharField(max_length=255, null=True)
    subtitle = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(default=datetime.now)
    started_at = models.DateTimeField(null=True, verbose_name=_('Beginning of this project'))
    ended_at = models.DateTimeField(null=True, verbose_name=_('Ending of this project'))
    country = CountryField(null=True)
    city = models.ForeignKey(City, null=True)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    archived = models.BooleanField(default=False)
    position = models.PositiveIntegerField(null=True)
    published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = ProjectSlug.objects.unique_slugify(self.name_en,
                                                           max_length=50)
        return super().save(*args, **kwargs)

    def get_media_path(self):
        return 'projects/%s' % self.slug

    def __str__(self):
        return self.slug

    class Meta:
        db_table = 'mnemotopy_project'
