from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


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


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredients, through='Recipes_Ingredients', related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tags, related_name='recipes'
    )
    # favorite = models.ManyToManyField(
    #     User, related_name='favorite_recipes', null=True
    # )
    image = models.ImageField(
        upload_to='recipes/images/',
    )
    name = models.CharField(max_length=200)
    text = models.TextField()
    cooking_time = models.IntegerField(validators=[MinValueValidator(1)])


class Recipes_Ingredients(models.Model):
    recipes = models.ForeignKey(
        Recipes, on_delete=models.CASCADE,
        related_name='ingredients_amount'
    )
    ingredients = models.ForeignKey(
        Ingredients, on_delete=models.CASCADE
    )
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.recipes} - {self.ingredients}'
