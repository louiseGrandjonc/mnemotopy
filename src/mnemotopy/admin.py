from django.contrib import admin

from linguist.admin import TranslatableModelAdmin

from mnemotopy.models import Tag, Category


class TagAdmin(TranslatableModelAdmin):
    list_display = ('slug', 'name_fr', 'name_en')

admin.site.register(Tag, TagAdmin)


class CategoryAdmin(TranslatableModelAdmin):
    list_display = ('slug', 'name_fr', 'name_en')

admin.site.register(Category, CategoryAdmin)
