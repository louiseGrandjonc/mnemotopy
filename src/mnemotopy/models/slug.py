import random

from django.conf import settings
from django.utils.text import slugify

from sluggable.models import Slug, SlugManager

from .category import Category


class ProjectSlugManager(SlugManager):
    def unique_slugify(self, from_string, max_length=None, instance=None):
        slug = slugify(from_string)
        forbidden_slugs = list(settings.FORBIDDEN_SLUGS) + list(Category.objects.all().values_list('name_en', flat=True))
        if max_length:
            slug = slug[0:max_length]
        available = self.is_slug_available(slug, obj=instance) and slug not in forbidden_slugs
        while not available:
            if max_length and len(slug) + 4 > max_length:
                slug = slug[0:max_length-4]
            slug = '%s-%d' % (slug, random.randint(1, 500))
            available = self.is_slug_available(slug, obj=instance) and slug not in forbidden_slugs

        return slug


class ProjectSlug(Slug):
    objects = ProjectSlugManager()

    class Meta:
        abstract = False
