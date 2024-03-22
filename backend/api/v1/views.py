from recipes.models import Tags
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializer import TagsSerializer


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
