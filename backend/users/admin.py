from django.contrib import admin
from recipes.models import Ingredients, Recipes, Shopping_Cart, Tags

from .models import Subscription, UserCustom


class SearchAdmin(admin.ModelAdmin):
    search_fields = ["^name"]


admin.site.register(Tags, SearchAdmin)
admin.site.register(Ingredients, SearchAdmin)
admin.site.register(UserCustom, SearchAdmin)
admin.site.register(Subscription, SearchAdmin)
admin.site.register(Recipes, SearchAdmin)
admin.site.register(Shopping_Cart, SearchAdmin)
