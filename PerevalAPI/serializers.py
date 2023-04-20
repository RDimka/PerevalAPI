from rest_framework import serializers
from .models import *


class UsersDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersData
        fields = '__all__'


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = '__all__'


class PerevalImagesSerializer(serializers.ModelSerializer):
    data = serializers.URLField()

    class Meta:
        model = PerevalImages
        fields = ('data', 'title',)


class PerevalSerializer(serializers.ModelSerializer):
    user = UsersDataSerializer()
    coords = CoordsSerializer()
    images = PerevalImagesSerializer(many=True)

    class Meta:
        model = PerevalAdded
        fields = ('id', 'user', 'beauty_title', 'title', 'other_titles', 'connect', 'coords', 'level_winter',
                  'level_spring', 'level_summer', 'level_autumn', 'images', 'status')

