from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
from django.urls import path

urlpatterns = [
    path('token/create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('companies/', views.CompanyListAPIView.as_view(), name='company_list'),
    path('companies/<int:id>/', views.CompanyDetailAPIView.as_view(), name='company_detail'),
    path('companies/<int:id>/vacancies/', views.CompanyVacanciesListAPIView.as_view(), name='company_vakancies_list'),

    path('vacancies/', views.VacancyListAPIView.as_view(), name='vacancy_list'),
    path('vacancies/top_ten/', views.TopTenVacanciesAPIView.as_view(), name='top_ten'),
    path('vacancies/<int:id>/', views.VacancyDetailAPIView.as_view(), name='vacancy_detail'),

    path('vacancies/<int:id>/submit/', views.submit_vacancy),
    path('users/create/', views.UserViewSet.as_view({'post': 'create_user'})),
]