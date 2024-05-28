from django.contrib import admin

from recipes.models import (Ingredients, RecipeFavorite, Recipes,
                            RecipesIngredients, ShoppingCart, Tags)

from .models import Subscription, UserModel


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
admin.site.register(RecipesIngredients, SearchAdmin)
admin.site.register(RecipeFavorite, SearchAdmin)
admin.site.register(ShoppingCart, SearchAdmin)
admin.site.register(UserModel, UserAdmin)
admin.site.register(Subscription, SearchAdmin)
