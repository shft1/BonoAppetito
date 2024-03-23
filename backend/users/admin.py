from django.contrib import admin
from recipes.models import Tags, Ingredients
from .models import UserCustom

admin.site.register(Tags)
admin.site.register(Ingredients)
admin.site.register(UserCustom)
