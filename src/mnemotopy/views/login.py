from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm

from mnemotopy.forms import AuthenticationForm

def login(request, template_name='mnemotopy/login.html', authentication_form=AuthenticationForm):
    return auth_views.login(request,
                            template_name=template_name,
                            authentication_form=authentication_form)
