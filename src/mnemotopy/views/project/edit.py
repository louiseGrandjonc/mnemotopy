from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic import CreateView, UpdateView, ListView, FormView

from mnemotopy.forms import ProjectForm, get_project_media_formset
from mnemotopy.models import Project


class ProjectViewMixin(object):
    model = Project
    form_class = ProjectForm
    template_name = 'mnemotopy/project/edit/detail.html'

    def get_success_url(self):
        return reverse('project_edit', kwargs={
            'pk': self.object.pk
        })

    def get_context_data(self, **kwargs):
        context = super(ProjectViewMixin, self).get_context_data(**kwargs)
        context['is_editing'] = True

        return context


class ProjectCreateView(ProjectViewMixin, CreateView):
    pass

create = login_required(ProjectCreateView.as_view())


class ProjectUpdateView(ProjectViewMixin, UpdateView):
    pk_url_kwarg = 'pk'

update = login_required(ProjectUpdateView.as_view())


class ProjectIndexView(ListView):
    model = Project
    paginate_by = 15
    template_name = 'mnemotopy/project/edit/index.html'

index = login_required(ProjectIndexView.as_view())


class ProjectMediaView(FormView):
    template_name = 'mnemotopy/project/edit/media/list.html'

    @cached_property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs.get('pk'))

    def get_success_url(self):
        return reverse('project_edit_media', kwargs={
            'pk': self.project.pk
        })

    def get_context_data(self, **kwargs):
        context = super(ProjectMediaView, self).get_context_data(**kwargs)
        context['project'] = self.project
        context['is_editing'] = True

        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form_class(self):
        return get_project_media_formset(self.project)

media = login_required(ProjectMediaView.as_view())
