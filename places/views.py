import json

from django.conf import settings
from django.shortcuts import render


def show_index(request):
    print("Кто-то зашёл на главную!")

    with open(
        settings.BASE_DIR / "static" / "places.json", encoding="utf-8"
    ) as f:
        places_geojson = json.load(f)

    return render(
        request, "index.html", {"places_geojson": json.dumps(places_geojson)}
    )
