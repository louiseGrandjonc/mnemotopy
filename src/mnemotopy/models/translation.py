from modeltranslation.translator import translator, TranslationOptions

from .tag import Tag
from .category import Category
from .project import Project
from .media import Media


class BaseTranslationOptions(TranslationOptions):
    fallback_undefined = ''


class TagTranslationOptions(BaseTranslationOptions):
    fields = ('name',)

translator.register(Tag, TagTranslationOptions)


class CategoryTranslationOptions(BaseTranslationOptions):
    fields = ('name', 'description')

translator.register(Category, CategoryTranslationOptions)


class ProjectTranslationOptions(BaseTranslationOptions):
    fields = ('name', 'subtitle', 'description')

translator.register(Project, ProjectTranslationOptions)


class MediaTranslationOptions(BaseTranslationOptions):
    fields = ('title',)

translator.register(Media, MediaTranslationOptions)
