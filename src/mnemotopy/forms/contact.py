from django.conf import settings
from django.core.mail import send_mail
from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(required=True, label='Your email address')
    subject = forms.CharField(required=False)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def send_email(self):
        subject = 'Sent from Mnemotopy Website: %s' % self.cleaned_data.get('subject', '')
        if not hasattr(settings, 'EMAIL_HOST'):
            return False

        try:
            send_mail(subject,
                      self.cleaned_data.get('message'),
                      self.cleaned_data.get('email'),
                      getattr(settings, 'EMAIL_TO', []))
        except:
            return False

        return True
