from colorfield.fields import ColorField
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

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


# class Favorite(models.Model):
#     recipes = models.ForeignKey(

#     )
#     users = models.ForeignKey(

#     )


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredients, through='Recipes_Ingredients'
    )
    tags = models.ManyToManyField(
        Tags, through='Recipes_Tags'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
    )
    name = models.CharField(max_length=200)
    text = models.TextField()
    cooking_time = models.IntegerField(validators=[MinValueValidator(1)])


class Recipes_Ingredients(models.Model):
    recipes = models.ForeignKey(
        Recipes, on_delete=models.CASCADE, related_name='ingredients'
    )
    ingredients = models.ForeignKey(
        Ingredients, on_delete=models.CASCADE, related_name='recipes'
    )
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.recipes} - {self.ingredients}'


class Recipes_Tags(models.Model):
    recipes = models.ForeignKey(
        Recipes, on_delete=models.CASCADE, related_name='tags'
    )
    tags = models.ForeignKey(
        Tags, on_delete=models.CASCADE, related_name='recipes'
    )

    def __str__(self):
        return f'{self.recipes} - {self.tags}'
