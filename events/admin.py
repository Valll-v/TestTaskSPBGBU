from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from events.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" width = "300"/>'.format(obj.image.url)) \
            if obj.image else format_html('Без изображения')

    image_tag.short_description = 'Image'

    list_display = ['id', 'image_tag', 'title', 'description', 'date']
    search_fields = ['title', 'description']
    list_filter = ['date', 'title']

