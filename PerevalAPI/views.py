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
    serializer_class = PerevalSerializer



