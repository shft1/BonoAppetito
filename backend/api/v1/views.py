from djoser.views import UserViewSet
from recipes.models import Ingredients, Tags
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.models import Subscription

from .serializers import (IngredientsSerializer, Subscribe_GET_Serializer,
                          Subscribe_POST_Serializer, TagsSerializer)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class SubscribeViewSet(ModelViewSet):
    serializer_class = Subscribe_POST_Serializer
    # serializer_class = Subscribe_GET_Serializer
    queryset = Subscription.objects.all()

    @action(detail=False, url_path='subscriptions')
    def get_subscriptions(self, request):
        subs = request.user.follow.all()
        serializer = self.get_serializer(subs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'delete'], url_path='subscribe')
    def post_del_subscriptions(self, request, pk):
        if request.method == 'POST':
            serializer = self.get_serializer(data={'follow': pk})
            if serializer.is_valid():
                serializer.save(user=self.request.user)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        Subscription.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
