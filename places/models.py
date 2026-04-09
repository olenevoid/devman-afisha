from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    description_short = models.TextField(verbose_name="Краткое описание")
    description_long = models.TextField(verbose_name="Полное описание")
    lng = models.FloatField(verbose_name="Долгота")
    lat = models.FloatField(verbose_name="Широта")

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="places/", verbose_name="Изображение")
    position = models.PositiveIntegerField(verbose_name="Позиция", default=0)

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
        ordering = ["position"]

    def __str__(self):
        return f"{self.place.title} — {self.position}"
