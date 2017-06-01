from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from mnemotopy.models import Project

from .base import TagsModelForm


class ProjectForm(TagsModelForm):
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

    started_at = forms.DateField(widget=forms.widgets.DateInput(
        format="%d/%m/%Y",
        attrs={
            'placeholder': _('Format DD/MM/YYYY')
        }))
    ended_at = forms.DateField(widget=forms.widgets.DateInput(
        format="%d/%m/%Y",
        attrs={
            'placeholder': _('Format DD/MM/YYYY')
        }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ['country', 'position', 'started_at', 'ended_at']:
            self.fields[field].required = False

    class Meta:
        model = Project
        fields = ('country', 'categories',
                  'archived', 'published', 'position',
                  'started_at', 'ended_at',
                  'name_en', 'name_fr', 'subtitle_en', 'subtitle_fr',
                  'description_en', 'description_fr')
