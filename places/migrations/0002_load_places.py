import json
from pathlib import Path

from django.db import migrations


def load_places_from_json(apps, schema_editor):
    Place = apps.get_model("places", "Place")
    static_dir = Path(__file__).resolve().parent.parent.parent / "static" / "places"

    for json_file in static_dir.glob("*.json"):
        with open(json_file, encoding="utf-8") as f:
            data = json.load(f)

        Place.objects.create(
            title=data["title"],
            description_short=data["description_short"],
            description_long=data["description_long"],
            lng=float(data["coordinates"]["lng"]),
            lat=float(data["coordinates"]["lat"]),
        )


def reverse_load(apps, schema_editor):
    Place = apps.get_model("places", "Place")
    Place.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("places", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_places_from_json, reverse_load),
    ]
