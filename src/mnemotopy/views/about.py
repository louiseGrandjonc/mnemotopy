from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, TemplateView

from mnemotopy.forms import ContactForm


class ContactView(FormView):
    template_name = 'mnemotopy/contact.html'
    form_class = ContactForm

    def form_valid(self, form):
        succeeded = form.send_email()

        if succeeded:
            messages.success(self.request, _('Your message has been sent. I will get back to you as soon as possible'))
        else:
            messages.error(self.request, _('There was an error while sending your message. Please try again later.'))

        response = HttpResponseRedirect(reverse('contact'))

        return response


contact = ContactView.as_view()


class AboutView(TemplateView):
    template_name = 'mnemotopy/about.html'


about = AboutView.as_view()
