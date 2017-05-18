from modeltranslation.translator import translator, TranslationOptions

from .tag import Tag
from .category import Category
from .project import Project
from .media import Media


class TagTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Tag, TagTranslationOptions)


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

translator.register(Category, CategoryTranslationOptions)


class ProjectTranslationOptions(TranslationOptions):
    fields = ('name', 'subtitle', 'description')

translator.register(Project, ProjectTranslationOptions)


class MediaTranslationOptions(TranslationOptions):
    fields = ('title',)

translator.register(Media, MediaTranslationOptions)
