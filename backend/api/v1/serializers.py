from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateMixin, UserSerializer
from recipes.models import Ingredients, Tags
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


class Subscribe_POST_Serializer(ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
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

        def validate(self, data):
            if data['user'] == data['follow']:
                raise serializers.ValidationError(
                    'Нельзя на себя подписываться!'
                )


class Subscribe_GET_Serializer(ModelSerializer):
    is_subscribed = serializers.BooleanField(read_only=True,
                                             default=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')
