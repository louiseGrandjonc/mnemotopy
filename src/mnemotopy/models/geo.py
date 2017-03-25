from __future__ import unicode_literals

from django.db import models

from django_countries.fields import CountryField


class City(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name="ascii name")
    slug = models.CharField(max_length=200)

    country = CountryField(null=True)

    class Meta:
        db_table = "cities_city"

    @property
    def parent(self):
        return self.region

    def __str__(self):
        if self.country:
            return '%s, %s' % (self.name, self.country)

        return self.name
