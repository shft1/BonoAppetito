from recipes.models import Ingredients, Tags
from rest_framework.serializers import ModelSerializer


class TagsSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Tags


class IngredientsSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Ingredients
