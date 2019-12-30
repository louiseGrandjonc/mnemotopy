from django.contrib.auth import views as auth_views, logout as logout_user
from django.urls import reverse
from django.http import HttpResponseRedirect


def logout(request):
    next_url = request.GET.get('next', reverse('home'))
    logout_user(request)

    return HttpResponseRedirect(next_url)
