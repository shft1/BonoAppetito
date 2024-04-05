import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateMixin, UserSerializer
from recipes.models import Ingredients, Recipes, Tags
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator
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
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


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
    is_subscribed = serializers.BooleanField(read_only=True, default=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')


class RecipeReadSerializer(ModelSerializer):
    pass


class ConvertToImage(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeCreateSerializer(ModelSerializer):
    image = ConvertToImage()
    # tags = TagsSerializer(many=True)

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'image', 'name', 'text', 'cooking_time')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        recipe = Recipes.objects.create(**validated_data)
        for tag in tags:
            recipe.tags.add(tag)
        return recipe
