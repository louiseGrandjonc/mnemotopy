from django.db import models
from django.utils import timezone as datetime


class Category(models.Model):
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(default=datetime.now)
    slug = models.SlugField()

    class Meta:
        db_table = 'mnemotopy_category'

    def __str__(self):
        return self.slug or ''
