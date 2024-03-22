from recipes.models import Tags
from rest_framework.serializers import ModelSerializer


class TagsSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Tags
