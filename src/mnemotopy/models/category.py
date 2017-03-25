from django.db import models
from django.utils import timezone as datetime
from django.utils.six import with_metaclass

from linguist.metaclasses import ModelMeta as LinguistMeta


class Category(with_metaclass(LinguistMeta, models.Model)):
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(default=datetime.now)
    slug = models.SlugField()

    class Meta:
        db_table = 'mnemotopy_category'
        linguist = {
            'identifier': 'category',
            'fields': ('name', 'description')
        }
