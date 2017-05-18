from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from mnemotopy.db.utils import queryset_to_dict
from mnemotopy.models import Project, Tag

from .base import CommaSeparatedCharField


class ProjectForm(forms.ModelForm):
    name_en = forms.CharField(label=_('Name'),
                              max_length=50,
                              required=True)
    subtitle_en = forms.CharField(label=_('Subtitle'),
                                  max_length=140,
                                  required=False)
    description_en = forms.CharField(label=_('Description'),
                                     widget=forms.Textarea(attrs={
                                         'class': 'rte'}),
                                     required=False)

    name_fr = forms.CharField(label=_('Name'),
                              max_length=50,
                              required=False)
    subtitle_fr = forms.CharField(label=_('Subtitle'),
                                  max_length=140,
                                  required=False)
    description_fr = forms.CharField(label=_('Description'),
                                     widget=forms.Textarea(attrs={
                                         'class': 'rte'}),
                                     required=False)

    tags = CommaSeparatedCharField(label=_('Tags'),
                                   required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ['country', 'position', 'started_at', 'ended_at']:
            self.fields[field].required = False

        if self.instance.pk:
            tags = self.instance.tags.all()
            self.initial['tags'] = ', '.join([tag.name for tag in tags])

        self.fields['started_at'].widget.attrs = {'class': 'hasDatepicker'}
        self.fields['ended_at'].widget.attrs = {'class': 'hasDatepicker'}

    def clean_tags(self):
        tag_values = self.cleaned_data.get('tags')
        tags = []
        if tag_values:
            existing_tags = queryset_to_dict(Tag.objects.filter(name_en__in=tag_values), key='name_en')
            tags = [Tag(name_en=tag, slug=slugify(tag))
                    for tag in [tag for tag in tag_values if tag not in existing_tags.keys()]] + list(existing_tags.values())

        return tags

    def save(self, *args, **kwargs):
        self.instance = super().save(*args, **kwargs)

        tags = self.cleaned_data.get('tags', [])
        for t in tags:
            t.save()
        self.instance.tags.set(tags)

        return self.instance

    class Meta:
        model = Project
        fields = ('country', 'categories',
                  'archived', 'published', 'position',
                  'started_at', 'ended_at',
                  'name_en', 'name_fr', 'subtitle_en', 'subtitle_fr',
                  'description_en', 'description_fr')
