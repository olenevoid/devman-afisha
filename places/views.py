import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from places.models import Place

DETAILS_URL_PLACEHOLDER = "/places/{place_id}/"


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
            "detailsUrl": DETAILS_URL_PLACEHOLDER.format(place_id=place.id),
        },
    }


def show_index(request):
    print("Кто-то зашёл на главную!")

    features = [serialize_place(place) for place in Place.objects.all()]

    places_geojson = json.dumps(
        {"type": "FeatureCollection", "features": features}
    )

    context = {"places_geojson": places_geojson}

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
    place = get_object_or_404(Place, pk=place_id)
    return JsonResponse(
        serialize_place_details(place),
        json_dumps_params={"ensure_ascii": False, "indent": 2},
    )
