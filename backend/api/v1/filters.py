from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from recipes.models import Recipes, Tags

User = get_user_model()


class RecipeFilter(filters.FilterSet):
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tags.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )

    class Meta:
        model = Recipes
        fields = ('author', 'tags',)
