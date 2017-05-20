import django
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from mnemotopy.models import Project, Category


class ProjectDetailTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name_en='architecture', description_en='archi', slug='archi')
        self.project = Project.objects.create(slug='mnemotopy',
                                              name_en='test',
                                              subtitle_en='test sub',
                                              description_en='hello')
        self.project.categories.add(self.category)

        self.user = User.objects.create(username='louise', is_superuser=True)
        self.user.set_password('secret')
        self.user.save()

    def test_get_unpublished_project(self):
        url = reverse('project_detail', args=[self.project.slug])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        self.client.login(username='louise', password='secret')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_project(self):
        project = self.project
        project.published = True
        project.save()

        url = reverse('project_detail', args=[project.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
