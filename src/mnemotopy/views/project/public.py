from django.http import Http404
from django.views.generic.detail import DetailView

from mnemotopy.models import Project


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'mnemotopy/project/detail/detail.html'
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not self.object.published and not (request.user.is_staff or request.user.is_superuser):
            raise Http404
        return response

project_detail = ProjectDetailView.as_view()
