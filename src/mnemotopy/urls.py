from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from mnemotopy.views.project import edit, public
from mnemotopy.views.login import logout
from mnemotopy.views.about import about, contact
from mnemotopy.forms import AuthenticationForm




# languages = '|'.join(dict(settings.LANGUAGES).keys())

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='mnemotopy/login.html',
                                                  authentication_form=AuthenticationForm)),
    url(r'^logout/$', logout,
        name='logout'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # url(r'^archive/$',
    #     public.archive,
    #     name='archive_index'),

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
    url(r'^edit/projects/(?P<pk>[\d]+)/media/(?P<media_pk>[\d]+)/delete/$',
        edit.delete_media,
        name='project_edit_delete_media'),
]

urlpatterns += i18n_patterns(
    url(r'^$',
        public.home,
        name='home'),
    url(r'^about/$',
        about,
        name='about'),
    url(r'^contact/$',
        contact,
        name='contact'),
    url(r'^categories/(?P<slugs>[\/\-a-zA-Z]+)/$',
        public.project_index,
        name='project_index'),
    url(r'^projects/(?P<slug>[\w.:@+-]+)/$',
        public.project_detail,
        name='project_detail'),
    prefix_default_language=False
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
