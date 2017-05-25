from django.conf import settings
from django.contrib.auth import views as auth_views, logout as logout_user
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from mnemotopy.forms import AuthenticationForm

def login(request, template_name='mnemotopy/login.html', authentication_form=AuthenticationForm):
    return auth_views.login(request,
                            template_name=template_name,
                            authentication_form=authentication_form)


def logout(request):
    next_url = request.GET.get('next', reverse('home'))
    logout_user(request)

    return HttpResponseRedirect(next_url)
