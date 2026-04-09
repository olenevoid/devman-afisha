from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from places.models import Place


def serialize_place(place):
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [place.lng, place.lat],
        },
        "properties": {
            "title": place.title,
            "placeId": place.id,
            "detailsUrl": reverse("place_details", args=[place.id]),
        },
    }


def show_index(request):
    print("Кто-то зашёл на главную!")

    features = [serialize_place(place) for place in Place.objects.all()]

    context = {
        "places_geojson": {"type": "FeatureCollection", "features": features}
    }

    return render(request, "index.html", context)


def serialize_place_details(place):
    return {
        "title": place.title,
        "imgs": [image.image.url for image in place.images.all()],
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lng": place.lng,
            "lat": place.lat,
        },
    }


def place_details(request, place_id):
    place = get_object_or_404(
        Place.objects.prefetch_related("images"), pk=place_id
    )
    return JsonResponse(
        serialize_place_details(place),
        json_dumps_params={"ensure_ascii": False, "indent": 2},
    )
