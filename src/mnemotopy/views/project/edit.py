from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from mnemotopy.forms import ProjectForm, MediaForm
from mnemotopy.models import Project, Media

from pure_pagination.paginator import Paginator


class ProjectViewMixin(object):
    section = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_editing'] = self.section

        return context


class ProjectFormViewMixin(ProjectViewMixin):
    model = Project
    form_class = ProjectForm
    template_name = 'mnemotopy/project/edit/detail.html'

    def get_success_url(self):
        return reverse('project_edit', kwargs={
            'pk': self.object.pk
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['project'] = self.object

        return context


class ProjectCreateView(ProjectFormViewMixin, CreateView):
    section = 'create'

create = login_required(ProjectCreateView.as_view())


class ProjectUpdateView(ProjectFormViewMixin, UpdateView):
    pk_url_kwarg = 'pk'
    section = 'update'

update = login_required(ProjectUpdateView.as_view())


class ProjectIndexView(ProjectViewMixin, ListView):
    model = Project
    paginate_by = 2
    paginator_class = Paginator
    template_name = 'mnemotopy/project/edit/index.html'
    section = 'index'

index = login_required(ProjectIndexView.as_view())


class MediaViewMixin(ProjectViewMixin):
    @cached_property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs.get('pk'))

    def get_queryset(self, *args, **kwargs):
        return self.project.medias.all()

    def get_success_url(self):
        return reverse('project_edit_update_media', kwargs={
            'pk': self.project.pk,
            'media_pk': self.object.pk
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        context['medias'] = self.project.medias.all()

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['project'] = self.project
        return kwargs


class ProjectMediaView(MediaViewMixin, ListView):
    section = 'media'
    model = Media
    template_name = 'mnemotopy/project/edit/media/list.html'

media_index = login_required(ProjectMediaView.as_view())


class MediaCreateView(MediaViewMixin, CreateView):
    model = Media
    form_class = MediaForm
    template_name = 'mnemotopy/project/edit/media/detail.html'

create_media = login_required(MediaCreateView.as_view())


class MediaUpdateView(MediaViewMixin, UpdateView):
    model = Media
    form_class = MediaForm
    template_name = 'mnemotopy/project/edit/media/detail.html'
    pk_url_kwarg = 'media_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media'] = self.object
        return context


update_media = login_required(MediaUpdateView.as_view())


class MediaDeleteView(MediaViewMixin, DeleteView):
    model = Media
    pk_url_kwarg = 'media_pk'

    def get_success_url(self):
        return reverse('project_edit_media', kwargs={
            'pk': self.project.pk,
        })

delete_media = MediaDeleteView.as_view()
