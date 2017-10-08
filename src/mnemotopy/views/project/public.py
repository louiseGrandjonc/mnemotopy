from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.generic import DetailView, ListView, TemplateView

import itertools

from mnemotopy.models import Project, Category


class Home(TemplateView):
    template_name = 'mnemotopy/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all().order_by('id')
        combinations = []

        for length in range(1, len(categories)+1):
            for subset in itertools.combinations(categories, length):
                combinations.append(subset)

        context['combinations'] = combinations

        return context

home = login_required(Home.as_view())


class ProjectIndexView(ListView):
    template_name = 'mnemotopy/project/index.html'

    def get_queryset(self):
        qs = Project.objects.filter(published=True).order_by('position', '-created_at')
        slugs = self.kwargs['slugs'].split('/')
        if 'all' not in slugs:
            categories = Category.objects.filter(slug__in=slugs)
            qs.filter(categories__in=categories)
        return qs

project_index = login_required(ProjectIndexView.as_view())


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'mnemotopy/project/detail/detail.html'
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not self.object.published and not (request.user.is_staff or request.user.is_superuser):
            raise Http404
        return response

project_detail = login_required(ProjectDetailView.as_view())
