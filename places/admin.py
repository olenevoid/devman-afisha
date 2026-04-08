from django.contrib import admin
from django.utils.html import format_html

from .models import Image, Place


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    readonly_fields = ["preview"]
    fields = ["image", "position", "preview"]

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:200px;" />', obj.image.url
            )
        return ""


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImageInline]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
