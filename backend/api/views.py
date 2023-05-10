from typing import OrderedDict

from .models import Company, Vacancy
from .serializers import CompanySerializer, VacancySerializer, CreateUserSerializer

from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework import generics, viewsets, status

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class CompanyListAPIView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyDetailAPIView(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'id'

class CompanyVacanciesListAPIView(generics.ListAPIView):
    serializer_class = VacancySerializer

    def get_queryset(self):
        company_id = self.kwargs.get('id')
        return Vacancy.objects.filter(company_id=company_id)

class VacancyListAPIView(generics.ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

class VacancyDetailAPIView(generics.RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    lookup_field = 'id'

class TopTenVacanciesAPIView(generics.ListAPIView):
    queryset = Vacancy.objects.order_by('-salary')[:10]
    serializer_class = VacancySerializer

@api_view(['POST'])
def submit_vacancy(request, id=None):
    if not request.user.is_authenticated:
        raise NotAuthenticated()
    vacancy = get_object_or_404(Vacancy, pk=id)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'vacancy_{vacancy.id}',
        {
            'type': 'vacancy_notification',
            'message': f'User {request.user.username} applied for the vacancy {vacancy.name}, {vacancy.id}'
        }
    )

    return Response({'status': 'success'})

class UserViewSet(viewsets.ViewSet):

    def create_user(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create(
            username=serializer.validated_data['username'],
            password=make_password(serializer.validated_data['password']),
            is_active=True
        )
        return Response({'message': 'User has benn successfully created'}, status=status.HTTP_201_CREATED)