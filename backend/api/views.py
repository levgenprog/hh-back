from rest_framework import generics, viewsets, status
from .models import Company, Vacancy
from .serializers import CompanySerializer, VacancySerializer
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

class UserViewSet(viewsets.ViewSet):
    user_services: services.UserServicesInterface = services.UserRepositoryV1()

    def create_user(self, request):
        serializer = serializers.CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.user_services.create_user(serializer.validated_data)
        return Response({'message': 'User has benn successfully created'}, status=status.HTTP_201_CREATED)