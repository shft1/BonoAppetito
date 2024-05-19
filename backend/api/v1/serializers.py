import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserSerializer
from rest_framework import exceptions, serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Ingredients, Recipe_Favorite, Recipes,
                            Recipes_Ingredients, Shopping_Cart, Tags)
from users.models import Subscription

User = get_user_model()


class TagsSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tags


class IngredientsSerializer(ModelSerializer):
    class Meta:
        model = Ingredients
        fields = '__all__'


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(
        method_name='check_is_subscribed'
    )

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def check_is_subscribed(self, obj):
        try:
            obj.subscriber.get(user=self.context['request'].user)
            return True
        except Subscription.DoesNotExist:
            return False
        except TypeError:
            return False


class FavoriteCreate(ModelSerializer):
    users = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Recipe_Favorite
        fields = ('recipes', 'users')

        validators = [
            UniqueTogetherValidator(
                queryset=Recipe_Favorite.objects.all(),
                fields=('recipes', 'users'),
                message='Этот рецепт уже в избранном!'
            )
        ]


class ShortRecipeRead(ModelSerializer):
    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeCreateSerializer(ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Subscription
        fields = ('user', 'follow',)

        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'follow'),
                message='Вы уже подписаны на этого пользователя.'
            )
        ]

    def validate_follow(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError(
                'Нельзя на себя подписываться!'
            )
        return value


class Subscribe_GET_Serializer(ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        method_name='check_is_subscribed'
    )
    recipes = serializers.SerializerMethodField(
        method_name='user_recipes'
    )
    recipes_count = serializers.SerializerMethodField(
        method_name='user_recipes_count'
    )

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed', 'recipes',
                  'recipes_count',)

    def user_recipes(self, obj):
        recipes_queryset = obj.recipes.all()
        limit = self.context['request'].query_params.get('recipes_limit')
        if limit:
            return ShortRecipeRead(
                recipes_queryset[:int(limit)], many=True).data
        return ShortRecipeRead(recipes_queryset, many=True).data

    def user_recipes_count(self, obj):
        return len(obj.recipes.all())

    def check_is_subscribed(self, obj):
        try:
            obj.subscriber.get(user=self.context['request'].user)
            return True
        except Subscription.DoesNotExist:
            return False
        except TypeError:
            return False


class IngredientsAmountRead(ModelSerializer):
    id = serializers.IntegerField(source='ingredients.id')
    name = serializers.CharField(source='ingredients.name')
    measurement_unit = serializers.CharField(
        source='ingredients.measurement_unit')

    class Meta:
        model = Recipes_Ingredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientsAmount(ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredients', queryset=Ingredients.objects.all(),
    )

    class Meta:
        model = Recipes_Ingredients
        fields = ('id', 'amount')


class ConvertToImage(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeCreateSerializer(ModelSerializer):
    image = ConvertToImage()
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    ingredients = IngredientsAmount(many=True, write_only=True, required=True)

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'author', 'ingredients',
                  'image', 'name', 'text', 'cooking_time')
        extra_kwargs = {'tags': {'required': True}}

    def validate_tags(self, value):
        if len(value) == 0:
            raise exceptions.ValidationError
        if len(value) != len(set(value)):
            raise exceptions.ValidationError
        return value

    def validate_ingredients(self, value):
        if len(value) == 0:
            raise exceptions.ValidationError
        list_id_amount = []
        for dict in value:
            if dict in list_id_amount:
                raise exceptions.ValidationError
            list_id_amount.append(dict)
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipes.objects.create(**validated_data)
        for tag in tags:
            recipe.tags.add(tag)
        for ingredient in ingredients:
            recipe.ingredients.add(
                ingredient["ingredients"],
                through_defaults={"amount": ingredient["amount"]}
            )
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image')
        instance.name = validated_data.get('name')
        instance.text = validated_data.get('text')
        instance.cooking_time = validated_data.get('cooking_time')
        instance.save()

        instance.tags.set(validated_data.get('tags'))
        instance.ingredients.clear()
        for ingredient in validated_data.get('ingredients'):
            instance.ingredients.add(
                ingredient["ingredients"],
                through_defaults={"amount": ingredient["amount"]}
            )
        return instance


class RecipeReadSerializer(ModelSerializer):
    tags = TagsSerializer(many=True, read_only=True)
    author = CustomUserSerializer()
    ingredients = IngredientsAmountRead(many=True, read_only=True,
                                        source='ingredients_amount')
    is_favorited = serializers.SerializerMethodField(
        method_name='check_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='check_is_in_shopping_cart'
    )

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time',
                  )

    def check_is_favorited(self, obj):
        try:
            user = self.context['request'].user
            if obj in user.favorite_recipes.all():
                return True
            return False
        except AttributeError:
            return False

    def check_is_in_shopping_cart(self, obj):
        try:
            user = self.context['request'].user
            if obj in user.recipe_in_shopping_cart.all():
                return True
            return False
        except AttributeError:
            return False


class ShoppingCreateSerializer(ModelSerializer):
    users = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Shopping_Cart
        fields = ('recipes', 'users')

        validators = [
            UniqueTogetherValidator(
                queryset=Shopping_Cart.objects.all(),
                fields=('recipes', 'users'),
                message='Этот рецепт уже в списке покупок!'
            )
        ]
