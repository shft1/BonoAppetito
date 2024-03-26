from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateMixin, UserSerializer
from recipes.models import Ingredients, Tags
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class TagsSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Tags


class IngredientsSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Ingredients


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')
