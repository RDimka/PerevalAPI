from rest_framework import serializers
from .models import *
from drf_writable_nested import WritableNestedModelSerializer


class UsersDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersData
        fields = '__all__'

    def save(self, **kwargs):
        self.is_valid()
        pass_user = UsersData.objects.filter(email=self.validated_data.get('email'))
        if pass_user.exists():
            return pass_user.first()
        else:
            return UsersData.objects.create(
                email=self.validated_data.get('email'),
                firstname=self.validated_data.get('firstname'),
                lastname=self.validated_data.get('lastname'),
                surname=self.validated_data.get('surname'),
                phone=self.validated_data.get('phone'),
            )

class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = '__all__'


class PerevalImagesSerializer(serializers.ModelSerializer):
    data = serializers.URLField()

    class Meta:
        model = PerevalImages
        fields = ('data', 'title',)


#class PerevalAddedSerializer(serializers.ModelSerializer):
class PerevalAddedSerializer(WritableNestedModelSerializer):
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

        #Если пользователь существует, используем существующую запись
        user_by_email = UsersData.objects.filter(email=user['email'])
        if user_by_email.exists():
            user_serializer = UsersDataSerializer(data=user)
            print("Юзер существует")
            user_serializer.is_valid(raise_exception=True)
            print("Юзер валид")
            user = user_serializer.save()
            print("Юзер сохранили")
        else:#если пользователь не существует, создаем его
            user = UsersData.objects.create(**user)

        coords = Coords.objects.create(**coords)
        pereval = PerevalAdded.objects.create(**validated_data, user=user, coords=coords)

        for image in images:
            data = image.pop('data')
            title = image.pop('title')
            PerevalImages.objects.create(pereval=pereval, data=data, title=title)

        return pereval

    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user

            data_user = data.get('user')

            validating_user_fields = [
                instance_user.lastname != data_user['lastname'],
                instance_user.firstname != data_user['firstname'],
                instance_user.surname != data_user['surname'],
                instance_user.phone != data_user['phone'],
                instance_user.email != data_user['email'],
            ]
            if data_user is not None and any(validating_user_fields):
                raise serializers.ValidationError({'Отклонено': 'Нельзя изменять данные пользователя'})
        return data
