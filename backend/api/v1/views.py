from djoser.views import UserViewSet
from recipes.models import Ingredients, Tags
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.models import Subscription, UserCustom

from .serializers import (IngredientsSerializer, Subscribe_GET_Serializer,
                          SubscribeCreateSerializer, TagsSerializer)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class SubscribeViewSet(ModelViewSet):
    queryset = Subscription.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return Subscribe_GET_Serializer
        else:
            return SubscribeCreateSerializer

    @action(detail=False, url_path='subscriptions')
    def get_subscriptions(self, request):
        subs_id_queryset = request.user.follow.values("follow")
        subs_id_list = [dict_id['follow'] for dict_id in subs_id_queryset]
        subs = UserCustom.objects.filter(pk__in=subs_id_list)
        serializer = self.get_serializer(subs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'delete'], url_path='subscribe')
    def post_del_subscriptions(self, request, pk):
        if request.method == 'POST':
            serializer = self.get_serializer(data={'follow': pk})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user = UserCustom.objects.get(pk=pk)
            return Response(Subscribe_GET_Serializer(user).data,
                            status=status.HTTP_201_CREATED)
        Subscription.objects.filter(user=request.user, follow=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
