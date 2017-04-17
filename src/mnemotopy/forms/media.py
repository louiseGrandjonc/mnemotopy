from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import BaseModelFormSet, modelformset_factory


from mnemotopy.models import Media


def get_project_media_formset(project, extra=1):
    class BaseMediaFormSet(BaseModelFormSet):
        def __init__(self, *args, **kwargs):
            self.project = project
            super().__init__(*args, **kwargs)
            self.queryset = Media.objects.filter(project=self.project, position__isnull=False).order_by('position')

    class MediaForm(forms.ModelForm):
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
            self.project = project
            super().__init__(*args, **kwargs)
            self.fields['type'].initial = self.instance.type or Media.IMAGE

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
            # TODO handle upload vimeo
            self.instance.project = self.project
            return super().save(*args, **kwargs)

        class Meta:
            model = Media
            fields = ('type', 'position', 'image', 'video',
                      'audio', 'thumbnail_file', 'languages')

    return modelformset_factory(Media,
                                formset=BaseMediaFormSet,
                                form=MediaForm,
                                extra=extra,
                                can_delete=True)
