import json
import urllib.request
from pathlib import Path

from django.core.files.base import ContentFile
from django.db import migrations

MAX_IMAGE_SIZE = 5 * 1024 * 1024


def load_images_from_json(apps, schema_editor):
    Place = apps.get_model("places", "Place")
    Image = apps.get_model("places", "Image")
    static_dir = (
        Path(__file__).resolve().parent.parent.parent / "static" / "places"
    )

    for json_file in static_dir.glob("*.json"):
        with open(json_file, encoding="utf-8") as f:
            data = json.load(f)

        place = Place.objects.filter(title=data["title"]).first()
        if not place:
            continue

        Image.objects.filter(place=place).delete()

        for position, img_url in enumerate(data.get("imgs", [])):
            try:
                req = urllib.request.Request(
                    img_url, headers={"User-Agent": "Mozilla/5.0"}
                )
                with urllib.request.urlopen(req, timeout=30) as response:
                    if (
                        int(response.headers.get("Content-Length", 0))
                        > MAX_IMAGE_SIZE
                    ):
                        continue
                    content = response.read()
                filename = Path(img_url).name
                Image.objects.create(
                    place=place,
                    position=position,
                    image=ContentFile(content, name=filename),
                )
            except Exception:
                continue


def reverse_load(apps, schema_editor):
    apps.get_model("places", "Place")
    Image = apps.get_model("places", "Image")
    static_dir = (
        Path(__file__).resolve().parent.parent.parent / "static" / "places"
    )

    titles = []
    for json_file in static_dir.glob("*.json"):
        with open(json_file, encoding="utf-8") as f:
            data = json.load(f)
        titles.append(data["title"])

    Image.objects.filter(place__title__in=titles).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("places", "0003_image"),
    ]

    operations = [
        migrations.RunPython(load_images_from_json, reverse_load),
    ]
