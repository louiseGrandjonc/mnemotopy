from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^projects/(?P<pk>[\d]+)/edit/$',
    #     name='project_edit'),
    # url(r'^projects/add/$',
    #     name='project_add'),
    # url(r'^projects/(?P<slug>[\w.:@+-]+)/$',
    #     name='project_detail'),
]
