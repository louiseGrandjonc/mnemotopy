from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _

from mnemotopy.models import Media
from mnemotopy.tasks import upload_to_vimeo, edit_vimeo_information

from .base import TagsModelForm


class MediaForm(TagsModelForm):
    title_en = forms.CharField(label=_('Title (english)'),
                               max_length=255,
                               required=False)
    title_fr = forms.CharField(label=_('Title (french)'),
                               max_length=255,
                               required=False)
    languages = forms.MultipleChoiceField(choices=settings.LANGUAGES,
                                          widget=forms.CheckboxSelectMultiple(),
                                          required=False)
    type = forms.ChoiceField(choices=Media.TYPE_CHOICES,
                             required=True,
                             widget=forms.RadioSelect(attrs={'class': 'radio-type'}))

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        super().__init__(*args, **kwargs)
        self.fields['type'].initial = self.instance.type or Media.IMAGE
        self.fields['position'].required = False

    def clean(self, *args, **kwargs):
        cleaned_data = self.cleaned_data

        if int(cleaned_data['type']) == Media.IMAGE and not cleaned_data.get('image', None):
            self.add_error('image', _('The image field is required for a media of type image'))

        if int(cleaned_data['type']) == Media.VIDEO and not cleaned_data.get('video', None):
            self.add_error('video', _('The video field is required for a media of type video'))

        if int(cleaned_data['type']) == Media.AUDIO:
            if not cleaned_data.get('audio', None):
                self.add_error('audio', _('The audio field is required for a media of type audio'))
            if not cleaned_data.get('thumbnail_file', None):
                self.add_error('thumbnail_file', _('The image field is required for a media of type audio'))

            return cleaned_data

    def save(self, *args, **kwargs):
        self.instance.project = self.project
        self.instance = super().save(*args, **kwargs)

        if self.instance.type == self.instance.VIDEO:
            if 'video' in self.changed_data or not self.instance.url:
                upload_to_vimeo.delay(self.instance.pk)
            else:
                edit_vimeo_information.delay(self.instance.pk, change_thumbnail='thumbnail_file' in self.changed_data)

        return self.instance

    class Meta:
        model = Media
        fields = ('type', 'position', 'image', 'video',
                  'audio', 'thumbnail_file', 'languages',
                  'title_en', 'title_fr', 'url',)
