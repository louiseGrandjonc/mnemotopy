from django.conf.urls import url
from django.contrib import admin

from mnemotopy.views.project import edit
from mnemotopy.views.login import login

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', login),
    url(r'^edit/projects/$',
        edit.index,
        name='project_edit_list'),
    url(r'^edit/projects/add/$',
        edit.create,
        name='project_add'),
    url(r'^edit/projects/(?P<pk>[\d]+)/$',
        edit.update,
        name='project_edit'),
    url(r'^edit/projects/(?P<pk>[\d]+)/media/$',
        edit.media,
        name='project_edit_media'),

    # url(r'^projects/(?P<slug>[\w.:@+-]+)/$',
    #     name='project_detail'),
]
