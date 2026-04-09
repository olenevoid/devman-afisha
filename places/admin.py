from adminsortable2.admin import SortableAdminBase, SortableTabularInline
from django.contrib import admin
from django.utils.html import format_html
from tinymce.widgets import TinyMCE

from .models import Image, Place


class ImageInline(SortableTabularInline):
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
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [ImageInline]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "long_description":
            kwargs["widget"] = TinyMCE()
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
