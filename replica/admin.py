from __future__ import absolute_import
from django.contrib import admin
from django.db import models
from .models import Media, Entry, Page

class MediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'url',)	

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'is_active', 'is_published', 'author')
    list_filter = ('is_active', 'post_type')
    exclude = ('summary_html', 'body_html')
    prepopulated_fields = {"slug": ("title",)}
    #formfield_overrides = {
    #        models.TextField: {'widget': EpicEditorWidget},
    #    }

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(EntryAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'body':
            formfield.widget.attrs['rows'] = 25
        return formfield

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'is_active', 'is_published')
    list_filter = ('is_active',)
    exclude = ('description_html', 'content_html')

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(PageAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'body':
            formfield.widget.attrs['rows'] = 25
        return formfield

admin.site.register(Media, MediaAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Page, PageAdmin)
