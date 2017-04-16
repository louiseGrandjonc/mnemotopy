import random

from django.conf import settings
from django.utils.text import slugify

from sluggable.models import Slug, SlugManager


class ProjectSlugManager(SlugManager):
    def unique_slugify(self, from_string, max_length=None, instance=None):
        slug = slugify(from_string)
        if max_length:
            slug = slug[0:max_length]
        available = self.is_slug_available(slug, obj=instance) and slug not in settings.FORBIDDEN_SLUGS
        while not available:
            if max_length and len(slug) + 4 > max_length:
                slug = slug[0:max_length-4]
            slug = '%s-%d' % (slug, random.randint(1, 500))
            available = self.is_slug_available(slug, obj=instance) and slug not in settings.FORBIDDEN_SLUG

        return slug


class ProjectSlug(Slug):
    objects = ProjectSlugManager()

    class Meta:
        abstract = False
