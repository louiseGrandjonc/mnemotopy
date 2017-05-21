from django.test import TestCase

from mnemotopy.forms import ProjectForm
from mnemotopy.models import Project, Category, Tag


class ProjectFormTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name_en='architecture', description_en='archi', slug='archi')
        self.project = Project.objects.create(slug='mnemotopy',
                                              name_en='test',
                                              subtitle_en='test sub',
                                              description_en='hello')
        self.project.categories.add(self.category)

    def test_create_project_errors(self):
        data = {
            'name_en': 'moriarty',
            'subtitle_en': 'history of violence',
            'description_en': 'video clip'
        }

        form = ProjectForm(data=data)
        self.assertFalse(form.is_valid())

    def test_create_project_complete(self):
        data = {
            'name_en': 'moriarty',
            'subtitle_en': 'history of violence',
            'description_en': 'video clip',
            'categories': [self.category]
        }

        form = ProjectForm(data=data)
        self.assertTrue(form.is_valid())

    def test_create_project_same_slug_category(self):
        data = {
            'name_en': 'architecture',
            'subtitle_en': 'history of violence',
            'description_en': 'video clip',
            'categories': [self.category]
        }

        form = ProjectForm(data=data)
        self.assertTrue(form.is_valid())

        project = form.save()
        self.assertNotEqual(project.slug, 'architecture')

    def test_update_project(self):
        data = {
            'name_en': 'moriarty',
            'subtitle_en': 'history of violence',
            'description_en': 'video clip',
            'categories': [self.category]
        }

        form = ProjectForm(data=data, instance=self.project)
        self.assertTrue(form.is_valid())
        project = form.save()

        project = Project.objects.get(pk=self.project.pk)

        self.assertEqual(project.name_en, 'moriarty')

    def test_create_tags(self):
        data = {
            'name_en': 'moriarty',
            'subtitle_en': 'history of violence',
            'description_en': 'video clip',
            'categories': [self.category],
            'tags': 'music, clip, Clement Deuve'
        }

        form = ProjectForm(data=data, instance=self.project)
        self.assertTrue(form.is_valid())
        form.save()

        self.assertEqual(Tag.objects.count(), 3)

        project = Project.objects.get(pk=self.project.pk)

        for tag in Tag.objects.all():
            tag in project.tags.all()

    def test_update_tags(self):
        data = {
            'name_en': 'moriarty',
            'subtitle_en': 'history of violence',
            'description_en': 'video clip',
            'categories': [self.category],
            'tags': 'music, clip, Clement Deuve'
        }

        form = ProjectForm(data=data, instance=self.project)
        self.assertTrue(form.is_valid())
        form.save()

        self.assertEqual(Tag.objects.count(), 3)

        project = Project.objects.get(pk=self.project.pk)

        for tag in Tag.objects.all():
            tag in project.tags.all()

        data['tags'] = 'music, video, Clement Deuve'

        form = ProjectForm(data=data, instance=self.project)
        self.assertTrue(form.is_valid())
        form.save()

        project = Project.objects.get(pk=self.project.pk)

        self.assertEqual(Tag.objects.count(), 4)

        tag = Tag.objects.get(name_en='clip')

        self.assertFalse(tag in project.tags.all())

        for tag in Tag.objects.exclude(name_en='clip'):
            self.assertTrue(tag in project.tags.all())
