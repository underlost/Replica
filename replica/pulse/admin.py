from __future__ import absolute_import
from django.contrib import admin
from django.db import models
from .models import Topic, Media, EntryType, Entry, Draft

def force_save(modeladmin, request, queryset):
    for item in queryset.iterator():
        item.save()
force_save.short_description = "Save Selected objects"


class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'user', 'is_public')
    list_filter = ('is_public',)
    prepopulated_fields = {"slug": ("title",)}

class MediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'user',)
    list_filter = ('user',)

class EntryTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user',)
    list_filter = ('user',)

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'is_active', 'post_type', 'user')
    list_filter = ('is_active', 'post_type')
    exclude = ('body_html',)
    prepopulated_fields = {"slug": ("title",)}
    list_per_page=250
    actions=[force_save, ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(EntryAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'body':
            formfield.widget.attrs['rows'] = 25
        return formfield

class DraftAdmin(admin.ModelAdmin):
    list_display = ('entry', 'title', 'last_edit',)
    list_filter = ('user',)

admin.site.register(Topic, TopicAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(EntryType, EntryTypeAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Draft, DraftAdmin)
