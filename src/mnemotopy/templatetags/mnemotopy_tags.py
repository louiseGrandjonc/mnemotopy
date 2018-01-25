from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def categories_url(**kwargs):
    categories = kwargs.get('categories', None)
    slugs = '/'.join([category.slug for category in categories])

    return reverse('project_index', kwargs={'slugs': slugs})


@register.filter(name='times')
def times(number):
    return range(number)
