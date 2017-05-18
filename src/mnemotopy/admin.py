from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from mnemotopy.models import Tag, Category, Project


class TagAdmin(TranslationAdmin):
    list_display = ('slug', 'name_fr', 'name_en')

admin.site.register(Tag, TagAdmin)


class CategoryAdmin(TranslationAdmin):
    list_display = ('slug', 'name_fr', 'name_en')

admin.site.register(Category, CategoryAdmin)


class ProjectAdmin(TranslationAdmin):
    list_display = ('slug', 'name_fr', 'name_en')

admin.site.register(Project, ProjectAdmin)
