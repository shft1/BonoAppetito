from djoser.views import UserViewSet
from recipes.models import Ingredients, Tags
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import IngredientsSerializer, TagsSerializer


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)
