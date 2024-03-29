from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientsViewSet, SubscribeViewSet, TagViewSet

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientsViewSet, basename='ingredient')
router.register('users', SubscribeViewSet, basename='subscribe')

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
