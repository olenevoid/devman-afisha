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
            self.stderr.write(
                self.style.ERROR(f"File not found: {json_file}")
            )
            return None

        with open(json_file, encoding="utf-8") as f:
            return json.load(f)

    def handle(self, *args, **options):
        filepath = options["filepath"]

        if filepath:
            data = self.load_json(filepath)
            if data is None:
                return
            data_sources = [(filepath, data)]
        else:
            static_dir = settings.BASE_DIR / "static" / "places"
            json_files = sorted(static_dir.glob("*.json"))

            if not json_files:
                self.stderr.write(self.style.ERROR("No JSON files found."))
                return

            data_sources = []
            for json_file in json_files:
                data = self.load_json(str(json_file))
                if data is not None:
                    data_sources.append((str(json_file), data))

        for source, data in data_sources:

            coordinates = data.get("coordinates", {})
            place, created = Place.objects.update_or_create(
                title=data["title"],
                defaults={
                    "description_short": data["description_short"],
                    "description_long": data["description_long"],
                    "lng": float(coordinates.get("lng", 0)),
                    "lat": float(coordinates.get("lat", 0)),
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created place: {place.title}")
                )
            else:
                self.stdout.write(f"Updated place: {place.title}")

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
