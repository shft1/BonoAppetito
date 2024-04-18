from djoser.views import UserViewSet
from recipes.models import Ingredients, Recipe_Favorite, Recipes, Tags
from rest_framework import exceptions, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.models import Subscription, UserCustom

from .serializers import (CustomUserSerializer, FavoriteCreate, FavoriteRead,
                          IngredientsSerializer, RecipeCreateSerializer,
                          RecipeReadSerializer, SubscribeCreateSerializer,
                          TagsSerializer)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


'''
class SubscribeViewSet(ModelViewSet):
    queryset = Subscription.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CustomUserSerializer
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
            return Response(CustomUserSerializer(user).data,
                            status=status.HTTP_201_CREATED)
        Subscription.objects.filter(user=request.user, follow=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''


class CustomUserViewSet(UserViewSet):

    @action(detail=False, url_path='subscriptions',
            serializer_class=CustomUserSerializer)
    def get_subscriptions(self, request):
        subs_id_queryset = request.user.follow.values("follow")
        subs_id_list = [dict_id['follow'] for dict_id in subs_id_queryset]
        subs = UserCustom.objects.filter(pk__in=subs_id_list)
        serializer = self.get_serializer(subs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'delete'],
            url_path='subscribe', serializer_class=SubscribeCreateSerializer)
    def post_del_subscriptions(self, request, id):
        if request.method == 'POST':
            serializer = self.get_serializer(data={'follow': id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user = UserCustom.objects.get(pk=id)
            return Response(
                CustomUserSerializer(user, context={'request': request}).data,
                status=status.HTTP_201_CREATED,
            )
        Subscription.objects.filter(user=request.user, follow=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipesViewSet(ModelViewSet):
    queryset = Recipes.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        else:
            return RecipeCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = self.perform_create(serializer)
        return Response(
            RecipeReadSerializer(
                recipe, context={'request': request}
            ).data, status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        new_recipe = self.perform_update(serializer)
        return Response(
            RecipeReadSerializer(
                new_recipe, context={'request': request}
            ).data, status=status.HTTP_200_OK
        )

    def perform_update(self, serializer):
        return serializer.save()

    @action(detail=True, methods=['post', 'delete'],
            url_path='favorite', serializer_class=FavoriteCreate)
    def post_del_favorite(self, request, pk):
        if request.method == 'POST':
            serializer = FavoriteCreate(
                data={'recipes': pk}, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            recipe = Recipes.objects.get(pk=pk)
            return Response(
                FavoriteRead(recipe).data,
                status=status.HTTP_201_CREATED
            )
        else:
            object = Recipe_Favorite.objects.filter(
                users=request.user, recipes=pk
            )
            if object:
                object.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(data={'errors': 'Такого рецепта нет в избранном!'},
                            status=status.HTTP_400_BAD_REQUEST)
