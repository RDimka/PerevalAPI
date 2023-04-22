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


class PerevalAddedSerializer(serializers.ModelSerializer):
    user = UsersDataSerializer()
    coords = CoordsSerializer()
    images = PerevalImagesSerializer(many=True)

    class Meta:
        model = PerevalAdded
        fields = ('id', 'user', 'beauty_title', 'title', 'other_titles', 'connect', 'coords', 'level_winter',
                  'level_spring', 'level_summer', 'level_autumn', 'images', 'status')

    def create(self, validated_data, **kwargs):
        user = validated_data.pop('user')
        coords = validated_data.pop('coords')
        images = validated_data.pop('images')

        user = UsersData.objects.create(**user)
        coords = Coords.objects.create(**coords)
        pereval = PerevalAdded.objects.create(**validated_data, user=user, coords=coords)

        for image in images:
            data = image.pop('data')
            title = image.pop('title')
            PerevalImages.objects.create(pereval=pereval, data=data, title=title)

        return pereval
