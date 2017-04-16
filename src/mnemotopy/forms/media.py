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
        title_en = forms.CharField(label=_('Name'),
                                   max_length=255,
                                   required=True)
        title_fr = forms.CharField(label=_('Name'),
                                   max_length=255,
                                   required=False)
        languages = forms.MultipleChoiceField(choices=settings.LANGUAGES,
                                              widget=forms.CheckboxSelectMultiple(),
                                              required=False)

        def __init__(self, *args, **kwargs):
            self.project = project
            super().__init__(*args, **kwargs)

            self.fields['type'].widget = forms.RadioSelect()

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
