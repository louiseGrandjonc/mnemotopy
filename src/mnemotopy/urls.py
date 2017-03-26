from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from mnemotopy.views.project import edit

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login),
    url(r'^projects/(?P<pk>[\d]+)/edit/$',
        edit.update,
        name='project_edit'),
    url(r'^projects/add/$',
        edit.create,
        name='project_add'),
    # url(r'^projects/(?P<slug>[\w.:@+-]+)/$',
    #     name='project_detail'),
]
