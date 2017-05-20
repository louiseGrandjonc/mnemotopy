from django.conf.urls import url
from django.contrib import admin

from mnemotopy.views.project import edit, public
from mnemotopy.views.login import login
from mnemotopy.views.user import change_language

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', login),
    url(r'^language/$', change_language,
        name='user_change_language'),

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
        edit.media_index,
        name='project_edit_media'),
    url(r'^edit/projects/(?P<pk>[\d]+)/media/add/$',
        edit.create_media,
        name='project_edit_create_media'),
    url(r'^edit/projects/(?P<pk>[\d]+)/media/(?P<media_pk>[\d]+)/$',
        edit.update_media,
        name='project_edit_update_media'),
    # url(r'^edit/projects/(?P<pk>[\d]+)/media/(?P<pk>[\d]+)/delete/$',
    #     edit.delete_media,
    #     name='project_edit_delete_media'),

    url(r'^projects/(?P<slug>[\w.:@+-]+)/$',
        public.project_detail,
        name='project_detail'),

    # url(r'^archive/$',
    #     public.archive,
    #     name='archive_index'),
]
