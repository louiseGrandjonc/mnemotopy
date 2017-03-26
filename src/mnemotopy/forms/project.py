from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _

from mnemotopy.models import Project


class ProjectForm(forms.ModelForm):
    name_en = forms.CharField(label=_('Name'),
                              max_length=50,
                              required=False)
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set initial values
        for field in self.instance._meta.linguist['fields']:
            for lang, _ in settings.LANGUAGES:
                field_name = '{0}_{1}'.format(field, lang)

                self.initial[field_name] = getattr(self.instance, field_name)

    def save(self, *args, **kwargs):
        for field in self.instance._meta.linguist['fields']:
            for lang, _ in settings.LANGUAGES:
                field_name = '%s_%s' % (field, lang)
                if getattr(self.cleaned_data, field_name):
                    setattr(self.instance, field_name, getattr(self.cleaned_data, field_name))
        return super().save(*args, **kwargs)

    class Meta:
        model = Project
        fields = ('slug', 'country', 'city', 'categories',
                  'tags', 'archived', 'published', 'position')
