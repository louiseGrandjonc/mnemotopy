from django.views.generic import CreateView, UpdateView, ListView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from mnemotopy.forms import ProjectForm
from mnemotopy.models import Project


class ProjectViewMixin(object):
    model = Project
    form_class = ProjectForm
    template_name = 'mnemotopy/project/edit/detail.html'

    def get_success_url(self):
        return reverse('project_edit', kwargs={
            'pk': self.object.pk
        })


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
