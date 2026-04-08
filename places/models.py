from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    description_short = models.CharField(
        max_length=500, verbose_name="Краткое описание"
    )
    description_long = models.TextField(verbose_name="Полное описание")
    lng = models.FloatField(verbose_name="Долгота")
    lat = models.FloatField(verbose_name="Широта")

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.title
