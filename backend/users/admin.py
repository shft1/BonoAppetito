from django.contrib import admin
from recipes.models import (Ingredients, Recipe_Favorite, Recipes,
                            Recipes_Ingredients, Shopping_Cart, Tags)

from .models import Subscription, UserCustom


class SearchAdmin(admin.ModelAdmin):
    search_fields = ['^name']


class UserAdmin(admin.ModelAdmin):
    list_filter = ['email', 'username']
    search_fields = ['^name']


class IngredientsAdmin(admin.ModelAdmin):
    list_filter = ['name']
    search_fields = ['^name']


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'favorite_count', 'pub_date']
    fields = ['name', 'text', 'author', 'image', 'tags',
              ('cooking_time', 'pub_date')]
    list_filter = ['name', 'author', 'tags']
    search_fields = ['^name']
    readonly_fields = ['pub_date']

    def favorite_count(self, obj):
        return obj.favorite.count()

    favorite_count.short_description = 'Кол-во в избранном'


admin.site.register(Tags, SearchAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Recipes, RecipeAdmin)
admin.site.register(Recipes_Ingredients, SearchAdmin)
admin.site.register(Recipe_Favorite, SearchAdmin)
admin.site.register(Shopping_Cart, SearchAdmin)
admin.site.register(UserCustom, UserAdmin)
admin.site.register(Subscription, SearchAdmin)
