from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientsViewSet, TagViewSet

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientsViewSet, basename='ingredient')

urlpatterns = [
    path('', include(router.urls))
]
