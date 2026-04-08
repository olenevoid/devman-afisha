import json

from django.shortcuts import render

from places.models import Place

DETAILS_URL_PLACEHOLDER = "/static/places/moscow_legends.json"


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
            "detailsUrl": DETAILS_URL_PLACEHOLDER,
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
