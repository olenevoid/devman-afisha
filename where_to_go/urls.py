from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from places.views import place_details, show_index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", show_index),
    path("places/<int:place_id>/", place_details, name="place_details"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
