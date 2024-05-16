from django.contrib import admin

from recipes.models import (Ingredients, Recipe_Favorite, Recipes,
                            Recipes_Ingredients, Shopping_Cart, Tags)

from .models import Subscription, UserCustom


class SearchAdmin(admin.ModelAdmin):
    search_fields = ["^name"]


class UserAdmin(admin.ModelAdmin):
    list_filter = ['email', 'username']
    search_fields = ['^name']


admin.site.register(Tags, SearchAdmin)
admin.site.register(Ingredients, SearchAdmin)
admin.site.register(Recipes, SearchAdmin)
admin.site.register(Recipes_Ingredients, SearchAdmin)
admin.site.register(Recipe_Favorite, SearchAdmin)
admin.site.register(Shopping_Cart, SearchAdmin)
admin.site.register(UserCustom, UserAdmin)
admin.site.register(Subscription, SearchAdmin)
