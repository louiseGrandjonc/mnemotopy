from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from linguist.helpers import prefetch_translations

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

        # set initial values
        for field in self.instance._meta.linguist['fields']:
            for lang, _ in settings.LANGUAGES:
                field_name = '{0}_{1}'.format(field, lang)

                self.initial[field_name] = getattr(self.instance, field_name)

        for field in ['country', 'position', 'started_at', 'ended_at']:
            self.fields[field].required = False

        if self.instance.pk:
            # fix django linguist, translated fields should be available for values_list
            tags = self.instance.tags.all()
            prefetch_translations(tags)
            self.initial['tags'] = ', '.join([tag.name for tag in tags])

        self.fields['started_at'].widget.attrs = {'class': 'hasDatepicker'}
        self.fields['ended_at'].widget.attrs = {'class': 'hasDatepicker'}

    def clean(self):
        tag_values = self.cleaned_data.get('tags')
        if tag_values:
            query = """SELECT tag.id, tag.created_at, tag.slug
                       FROM mnemotopy_tag tag INNER JOIN linguist_translation linguist ON (linguist.object_id=tag.id AND identifier='tag')
                       WHERE linguist.field_name='name' AND linguist.language='en' AND linguist.field_value IN %s"""

            existing_tags = queryset_to_dict(Tag.objects.raw(query, params=[tuple(tag_values)]), key='name_en')
            created_tags = [Tag(name_en=tag, slug=slugify(tag)) for tag in [tag for tag in tag_values if tag not in existing_tags.keys()]]
            for tag in created_tags:
                # needed for linguist -- Linguist should bulk create translations !
                tag.save()

            self.cleaned_data['tags'] = created_tags + list(existing_tags.values())

        return self.cleaned_data

    def save(self, *args, **kwargs):
        for field in self.instance._meta.linguist['fields']:
            for lang, _ in settings.LANGUAGES:
                field_name = '%s_%s' % (field, lang)
                if self.cleaned_data.get(field_name, None):
                    setattr(self.instance, field_name, self.cleaned_data.get(field_name))

        self.instance = super().save(*args, **kwargs)

        tags = self.cleaned_data.get('tags')
        if tags:
            self.instance.tags.set(tags)

        return self.instance

    class Meta:
        model = Project
        fields = ('country', 'categories',
                  'archived', 'published', 'position',
                  'started_at', 'ended_at')
