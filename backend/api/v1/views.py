from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import (Ingredients, RecipeFavorite, Recipes, ShoppingCart,
                            Tags)
from users.models import Subscription

from .filters import RecipeFilter
from .pagination import CustomPagination
from .permissions import RecipePermission
from .serializers import (FavoriteCreate, IngredientsSerializer,
                          RecipeCreateSerializer, RecipeReadSerializer,
                          ShoppingCreateSerializer, ShortRecipeRead,
                          SubscribeCreateSerializer, SubscribeGetSerializer,
                          TagsSerializer)

User = get_user_model()


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class UserViewSetMix(UserViewSet):
    pagination_class = CustomPagination

    @action(detail=False, url_path='subscriptions',
            serializer_class=SubscribeGetSerializer)
    def get_subscriptions(self, request):
        queryset = request.user.subscribe.all()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post'],
            url_path='subscribe', serializer_class=SubscribeCreateSerializer,
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request, id):
        user = get_object_or_404(User, pk=id)
        serializer = self.get_serializer(data={'follow': id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            SubscribeGetSerializer(user, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )

    @subscriptions.mapping.delete
    def del_subscriptions(self, request, id):
        get_object_or_404(User, pk=id)
        object_sub = Subscription.objects.filter(user=request.user, follow=id)
        if object_sub:
            object_sub.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            data={'errors': 'Вы не были подписаны на этого пользователя!'},
            status=status.HTTP_400_BAD_REQUEST
        )


class RecipesViewSet(ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (RecipePermission,)

    def get_queryset(self):
        query_params = self.request.query_params
        user = self.request.user
        if query_params.get('is_favorited'):
            try:
                return user.favorite_recipes.all()
            except AttributeError:
                return None
        if query_params.get('is_in_shopping_cart'):
            try:
                return user.recipe_shopping_cart.all()
            except AttributeError:
                return None
        return Recipes.objects.all()

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
            instance, data=request.data,
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

    @action(detail=True, methods=['post'], url_path='favorite',)
    def favorites(self, request, pk):
        serializer = FavoriteCreate(
            data={'recipes': pk}, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        recipe = Recipes.objects.get(pk=pk)
        return Response(
            ShortRecipeRead(recipe).data,
            status=status.HTTP_201_CREATED
        )

    @favorites.mapping.delete
    def del_favorite(self, request, pk):
        get_object_or_404(Recipes, pk=pk)
        object_fav = RecipeFavorite.objects.filter(
            users=request.user, recipes=pk
        )
        if object_fav:
            object_fav.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            data={'errors': 'Такого рецепта нет в избранном!'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'], url_path='shopping_cart')
    def shopping_cart(self, request, pk):
        serializer = ShoppingCreateSerializer(
            data={'recipes': pk}, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        recipe = Recipes.objects.get(pk=pk)
        return Response(
            ShortRecipeRead(recipe).data,
            status=status.HTTP_201_CREATED
        )

    @shopping_cart.mapping.delete
    def del_shopping_cart(self, request, pk):
        get_object_or_404(Recipes, pk=pk)
        object_shop = ShoppingCart.objects.filter(
            users=request.user, recipes=pk
        )
        if object_shop:
            object_shop.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            data={'errors': 'Такого рецепта нет в списке покупок!'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'], url_path='download_shopping_cart')
    def get_shopping_cart(self, request):
        un = dict()
        recipes_in_shopping_cart = request.user.recipe_shopping_cart.all()
        for recipe in recipes_in_shopping_cart:
            ingredients_for_recipe = recipe.recipes_ingredients.values(
                'amount', 'ingredients__name', 'ingredients__measurement_unit'
            )
            for ingredient in ingredients_for_recipe:
                ingredient_name = ingredient['ingredients__name']
                amount = ingredient['amount']
                measurement_unit = ingredient['ingredients__measurement_unit']
                if ingredient_name in un:
                    un[ingredient_name] = {
                        'name': ingredient_name,
                        'amount': un[ingredient_name]['amount'] + amount,
                        'measurement_unit': measurement_unit
                    }
                else:
                    un[ingredient_name] = {
                        'name': ingredient_name,
                        'amount': amount,
                        'measurement_unit': measurement_unit
                    }
        context = {'ingredients': un.values()}
        shopping_cart = render_to_string(
            'shopping_cart.html', context=context
        )
        response = HttpResponse(content_type='text/html')
        header = 'attachment; filename="shopping_cart.html"'
        response['Content-Disposition'] = header
        response.write(shopping_cart)
        return response
