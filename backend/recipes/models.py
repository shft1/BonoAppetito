from colorfield.fields import ColorField
from django.db import models


class Ingredients(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return self.name[:25]


class Tags(models.Model):
    name = models.CharField(max_length=200)
    color = ColorField(null=True)
    slug = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.slug[:25]
