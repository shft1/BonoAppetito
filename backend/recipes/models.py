from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredients(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Имя'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Размерность'
    )

    def __str__(self):
        return self.name[:25]

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tags(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Уникальное имя'
    )
    color = ColorField(
        unique=True,
        verbose_name='Цвет тега'
    )
    slug = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Уникальный слаг'
    )

    def __str__(self):
        return self.slug[:25]

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='Recipes_Ingredients',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tags,
        related_name='recipes',
        verbose_name='Теги'
    )
    favorite = models.ManyToManyField(
        User,
        through='Recipe_Favorite',
        related_name='favorite_recipes'
    )
    shopping_cart = models.ManyToManyField(
        User,
        through='Shopping_Cart',
        related_name='recipe_in_shopping_cart'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Фотография'
    )
    name = models.CharField(
        max_length=200,
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
        return self.name[:25]

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'


class Recipes_Ingredients(models.Model):
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='ingredients_amount',
        verbose_name='Рецепты'
    )
    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='recipes_amount',
        verbose_name='Ингредиенты'
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Кол-во ингредиента'
    )

    def __str__(self):
        return f'{self.recipes} - {self.ingredients}'

    class Meta:
        verbose_name = 'рецепт с ингредиентами'
        verbose_name_plural = 'Рецепты с Ингредиентами'


class Recipe_Favorite(models.Model):
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='users_favorite',
        verbose_name='Рецепты'
    )
    users = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes_favorite',
        verbose_name='Пользователи'
    )

    def __str__(self):
        return f'{self.users} - {self.recipes}'

    class Meta:
        verbose_name = 'избранное у пользователя'
        verbose_name_plural = 'Избранное у пользователей'


class Shopping_Cart(models.Model):
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='users_shopping_cart',
        verbose_name='Рецепты'
    )
    users = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes_shopping_cart',
        verbose_name='Пользователи'
    )

    def __str__(self):
        return f'{self.users} - {self.recipes}'

    class Meta:
        verbose_name = 'рецепт в списке покупок у пользователя'
        verbose_name_plural = 'Рецепты в списке покупок у пользователей'
