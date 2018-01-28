from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.views.generic import DetailView, ListView, TemplateView

from django_user_agents.utils import get_user_agent

import itertools

from mnemotopy.models import Project, Category, Media


class Home(TemplateView):
    template_name = 'mnemotopy/under_construction.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all().order_by('id')
        combinations = []

        for length in range(1, len(categories)+1):
            for subset in itertools.combinations(categories, length):
                combinations.append(subset)

        context['combinations'] = combinations

        return context


home = Home.as_view()


class ProjectIndexView(ListView):
    template_name = 'mnemotopy/project/index.html'

    def get_queryset(self):
        qs = Project.objects.filter(published=True,
                                    archived=False).order_by('position', '-created_at')
        slugs = self.kwargs['slugs'].split('/')
        if 'all' not in slugs:
            self.categories = Category.objects.filter(slug__in=slugs)
            for category in self.categories:
                qs = qs.filter(categories__in=[category])

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.categories
        return context

project_index = login_required(ProjectIndexView.as_view())


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'mnemotopy/project/detail/detail.html'
    slug_url_kwarg = 'slug'

    def get_template_names(self):
        user_agent = get_user_agent(self.request)
        if user_agent.is_mobile or user_agent.is_tablet:
            return ['mnemotopy/project/detail/detail_mobile.html', ]

        return ['mnemotopy/project/detail/detail.html', ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        medias = self.object.medias.order_by('position', 'id')
        context['medias'] = medias

        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not self.object.published and not (request.user.is_staff or request.user.is_superuser):
            raise Http404
        return response


project_detail = ProjectDetailView.as_view()


class MediaDetailView(DetailView):
    model = Media
    template_name = 'mnemotopy/project/detail/slideshow_detail.html'
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        self.slug = self.kwargs['slug']

        return Media.objects.filter(project__slug=self.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        next_media = self.object.next_media()
        if next_media:
            context['next_media_url'] = reverse('media_detail', kwargs={'slug': self.slug,
                                                                        'pk': next_media.pk})

        return context


media_detail = login_required(MediaDetailView.as_view())
