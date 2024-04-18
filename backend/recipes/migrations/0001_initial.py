# Generated by Django 3.2.16 on 2024-04-18 13:42

import colorfield.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('measurement_unit', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe_Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='recipes/images/')),
                ('name', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('cooking_time', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL)),
                ('favorite', models.ManyToManyField(related_name='favorite_recipes', through='recipes.Recipe_Favorite', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('color', colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=25, null=True, samples=None)),
                ('slug', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recipes_Ingredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('ingredients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredients')),
                ('recipes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_amount', to='recipes.recipes')),
            ],
        ),
        migrations.AddField(
            model_name='recipes',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='recipes.Recipes_Ingredients', to='recipes.Ingredients'),
        ),
        migrations.AddField(
            model_name='recipes',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='recipes.Tags'),
        ),
        migrations.AddField(
            model_name='recipe_favorite',
            name='recipes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_favorite', to='recipes.recipes'),
        ),
        migrations.AddField(
            model_name='recipe_favorite',
            name='users',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes_favorite', to=settings.AUTH_USER_MODEL),
        ),
    ]
