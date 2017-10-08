from django import forms
from django.core import validators
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from mnemotopy.db.utils import queryset_to_dict
from mnemotopy.models import Tag


class CommaSeparatedCharField(forms.Field):
    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return []

        value = [item.strip() for item in value.split(',') if item.strip()]
        value = list(set(value))

        return value

    def clean(self, value):
        value = self.to_python(value)
        self.validate(value)
        self.run_validators(value)
        return value


class TagsModelForm(forms.ModelForm):
    tags = CommaSeparatedCharField(label=_('Tags'),
                                   required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            tags = self.instance.tags.all()
            self.initial['tags'] = ', '.join([tag.name for tag in tags])

    def clean_tags(self):
        tag_slugs = [slugify(tag) for tag in self.cleaned_data.get('tags')]
        tags = []
        if tag_slugs:
            existing_tags = queryset_to_dict(Tag.objects.filter(slug__in=tag_slugs), key='slug')
            tags = [Tag(name_en=tag, slug=slugify(tag))
                    for tag in [tag for tag in tag_slugs if tag not in existing_tags.keys()]] + list(existing_tags.values())

        return tags

    def save(self, *args, **kwargs):
        tags = self.cleaned_data.pop('tags', [])

        self.instance = super().save(*args, **kwargs)

        for t in tags:
            t.save()

        self.instance.tags.set(tags)

        return self.instance
