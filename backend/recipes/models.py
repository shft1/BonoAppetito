from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()

MAX_LENGH = 200
SHORT_LENGTH = 25


class Ingredients(models.Model):
    name = models.CharField(
        max_length=MAX_LENGH,
        verbose_name='Имя'
    )
    measurement_unit = models.CharField(
        max_length=MAX_LENGH,
        verbose_name='Размерность'
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name[:SHORT_LENGTH]


class Tags(models.Model):
    name = models.CharField(
        max_length=MAX_LENGH,
        unique=True,
        verbose_name='Уникальное имя'
    )
    color = ColorField(
        unique=True,
        verbose_name='Цвет тега'
    )
    slug = models.CharField(
        max_length=MAX_LENGH,
        unique=True,
        verbose_name='Уникальный слаг'
    )

    def __str__(self):
        return self.slug[:SHORT_LENGTH]

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecipesIngredients'
    )
    tags = models.ManyToManyField(
        Tags,
        verbose_name='Теги'
    )
    favorite = models.ManyToManyField(
        User,
        through='RecipeFavorite',
        related_name='favorite_recipes'
    )
    user_shopping_cart = models.ManyToManyField(
        User,
        through='ShoppingCart',
        related_name='recipe_shopping_cart'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Фотография'
    )
    name = models.CharField(
        max_length=MAX_LENGH,
        verbose_name='Имя'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Время приготовления'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    def __str__(self):
        return self.name[:SHORT_LENGTH]

    class Meta:
        ordering = ['-pub_date']
        default_related_name = 'recipes'
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'


class RecipesIngredients(models.Model):
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепты'
    )
    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Ингредиенты'
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Кол-во ингредиента'
    )

    def __str__(self):
        return f'{self.recipes} - {self.ingredients}'

    class Meta:
        default_related_name = 'recipes_ingredients'
        verbose_name = 'рецепт с ингредиентами'
        verbose_name_plural = 'Рецепты с Ингредиентами'


class RecipeFavorite(models.Model):
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепты'
    )
    users = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователи'
    )

    def __str__(self):
        return f'{self.users} - {self.recipes}'

    class Meta:
        default_related_name = 'recipe_favorite'
        verbose_name = 'избранное у пользователя'
        verbose_name_plural = 'Избранное у пользователей'


class ShoppingCart(models.Model):
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепты'
    )
    users = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователи'
    )

    class Meta:
        default_related_name = 'shopping_cart'
        verbose_name = 'рецепт в списке покупок у пользователя'
        verbose_name_plural = 'Рецепты в списке покупок у пользователей'

    def __str__(self):
        return f'{self.users} - {self.recipes}'
