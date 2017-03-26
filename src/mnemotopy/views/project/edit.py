from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from mnemotopy.forms import ProjectForm
from mnemotopy.models import Project


class ProjectViewMixin(object):
    model = Project
    form_class = ProjectForm
    template_name = 'mnemotopy/project/edit.html'


class ProjectCreateView(ProjectViewMixin, CreateView):
    def get_success_url(self):
        return reverse('project_edit', kwargs={
            'pk': self.form.instance.pk
        })

create = login_required(ProjectCreateView.as_view())


class ProjectUpdateView(ProjectViewMixin, UpdateView):
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse('project_edit', kwargs={
            'pk': self.object.pk
        })

update = login_required(ProjectUpdateView.as_view())
