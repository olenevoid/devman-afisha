import json
import urllib.request
from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from places.models import Image, Place

MAX_IMAGE_SIZE = 5 * 1024 * 1024


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("filepath", type=str, nargs="?", default=None)

    def load_json(self, path):
        if path.startswith(("http://", "https://")):
            with urllib.request.urlopen(path, timeout=30) as response:
                return json.loads(response.read())

        json_file = Path(path)
        if not json_file.exists():
            self.stderr.write(self.style.ERROR(f"File not found: {json_file}"))
            return None

        with open(json_file, encoding="utf-8") as f:
            return json.load(f)

    def handle(self, *args, **options):
        filepath = options["filepath"]

        if filepath:
            place_record = self.load_json(filepath)
            if place_record is None:
                return
            places_to_load = [(filepath, place_record)]
        else:
            static_dir = settings.BASE_DIR / "static" / "places"
            json_files = sorted(static_dir.glob("*.json"))

            if not json_files:
                self.stderr.write(self.style.ERROR("No JSON files found."))
                return

            places_to_load = []
            for json_file in json_files:
                place_record = self.load_json(str(json_file))
                if place_record is not None:
                    places_to_load.append((str(json_file), place_record))

        for source, place_record in places_to_load:

            required_fields = ["title", "coordinates"]
            missing = [f for f in required_fields if f not in place_record]
            if missing:
                self.stderr.write(
                    self.style.ERROR(
                        f"Skipping {source}: missing fields: "
                        f"{', '.join(missing)}"
                    )
                )
                continue

            coordinates = place_record["coordinates"]
            missing_coords = [
                c for c in ("lng", "lat") if c not in coordinates
            ]
            if missing_coords:
                self.stderr.write(
                    self.style.ERROR(
                        f"Skipping {source}: coordinates missing: "
                        f"{', '.join(missing_coords)}"
                    )
                )
                continue

            place, created = Place.objects.update_or_create(
                title=place_record["title"],
                lng=float(coordinates["lng"]),
                lat=float(coordinates["lat"]),
                defaults={
                    "short_description": place_record.get(
                        "description_short", ""
                    ),
                    "long_description": place_record.get(
                        "description_long", ""
                    ),
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created place: {place.title}")
                )
            else:
                self.stdout.write(f"Updated place: {place.title}")

            Image.objects.filter(place=place).delete()

            for position, img_url in enumerate(place_record.get("imgs", [])):
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
                    self.stderr.write(
                        self.style.WARNING(
                            f"Failed to download image: {img_url}"
                        )
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Done: {place.title} — {place.images.count()} images"
                )
            )
