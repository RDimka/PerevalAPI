# Create your views here.
from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets

# Create your views here.

class UsersDataViewSet(viewsets.ModelViewSet):
    queryset = UsersData.objects.all()
    serializer_class = UsersDataSerializer


class CoordsViewSet(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer


class PerevalImagesViewSet(viewsets.ModelViewSet):
    queryset = PerevalImages.objects.all()
    serializer_class = PerevalImagesSerializer


class PerevalAddedViewSet(viewsets.ModelViewSet):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalAddedSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = 200 if response.status_code == 201 else response.status_code

        response_data = {'status': response.status_code,
                        'message': response.status_text,
                        'id': response.data['id'] if response.status_code == 200 else None,
                        }
        response.data = response_data
        return response


