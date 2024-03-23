from django.contrib import admin
from recipes.models import Ingredients, Tags

from .models import UserCustom


class SearchAdmin(admin.ModelAdmin):
    search_fields = ["^name"]


admin.site.register(Tags, SearchAdmin)
admin.site.register(Ingredients, SearchAdmin)
admin.site.register(UserCustom, SearchAdmin)
