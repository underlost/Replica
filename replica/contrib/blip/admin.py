from __future__ import absolute_import

from django.contrib import admin
from .models import Timeline, Blip


admin.site.register(Blip,
    list_display=["timeline", "pub_date", "is_private"],
    list_filter=["timeline", "is_private"],
    raw_id_fields=['user'],
    list_per_page=500,
)

admin.site.register(Timeline,
    prepopulated_fields={'slug': ('name',)},
)
