from django import forms
from django.core import validators
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from mnemotopy.db.utils import queryset_to_dict
from mnemotopy.models import Tag

from .widgets import MultiSelectWidget

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
    new_tags = CommaSeparatedCharField(label=_('Add new tags'),
                                       required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['tags'].widget = MultiSelectWidget(choices=[(tag.pk, tag.name) for tag in Tag.objects.all()])

    def clean_new_tags(self):
        tag_slugs = [slugify(tag) for tag in self.cleaned_data.get('new_tags')]
        tags = []
        if tag_slugs:
            existing_tags = queryset_to_dict(Tag.objects.filter(slug__in=tag_slugs), key='slug')
            tags = [Tag(name_en=tag, slug=slugify(tag))
                    for tag in [tag for tag in tag_slugs if tag not in existing_tags.keys()]] + list(existing_tags.values())

        return tags

    def save(self, *args, **kwargs):
        tags = self.cleaned_data.pop('new_tags', [])

        self.instance = super().save(*args, **kwargs)

        for t in tags:
            t.save()

        tags += list(self.cleaned_data.pop('tags', []))

        self.instance.tags.set(tags)

        return self.instance
