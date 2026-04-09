from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    short_description = models.TextField(
        verbose_name="Краткое описание", blank=True
    )
    long_description = models.TextField(
        verbose_name="Полное описание", blank=True
    )
    lng = models.FloatField(verbose_name="Долгота")
    lat = models.FloatField(verbose_name="Широта")

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Место",
    )
    image = models.ImageField(upload_to="places/", verbose_name="Изображение")
    position = models.PositiveIntegerField(verbose_name="Позиция", default=0)

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
        ordering = ["position"]
        indexes = [
            models.Index(fields=["position"]),
        ]

    def __str__(self):
        return f"{self.place.title} — {self.position}"
