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
    filterset_fields = ('user__email',)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        if response.status_code == 201:
            response.status_code = 200
            response_data = {'status': response.status_code,
                            'message': None,
                            'id': response.data['id']
                            }
        elif response.status_code == 400:
            response_data = {'status': response.status_code,
                            'message': 'Bad Request',
                            'id': None
                            }
        elif response.status_code == 500:
            response_data = {'status': response.status_code,
                            'message': 'Ошибка подключения к базе данных',
                            'id': None
                            }
        return response

    def partial_update(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        pereval = self.get_object()

        if pereval.status == 'new':
            serializer = PerevalAddedSerializer(pereval, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response_data = {'status': '1',
                                 'message': 'Изменения сохранены'
                                }
                return response
            else:
                response_data = {'status': '0',
                                 'message': serializer.errors
                                 }
                return response

        else:
            response_data = {'status': '0',
                             'message': f"Отклонено! Причина: {pereval.get_status_display()}"
                             }
            return response


