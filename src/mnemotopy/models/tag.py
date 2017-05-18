from django.db import models
from django.utils import timezone as datetime
from django.utils.six import with_metaclass


class Tag(models.Model):
    name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    slug = models.SlugField()

    class Meta:
        db_table = 'mnemotopy_tag'

    def __str__(self):
        return self.slug or ''
