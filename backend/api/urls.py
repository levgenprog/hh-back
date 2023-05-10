from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views
from django.urls import path

urlpatterns = [

    path('token/create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('companies/', views.CompanyViewSet.as_view({'get': 'get_companies'})),
    path('companies/<int:pk>/', views.CompanyViewSet.as_view({'get': 'get_company'})),
    path('companies/<int:pk>/vacancies/', views.CompanyViewSet.as_view({'get': 'get_company_vacancies'})),

    path('vacancies/', views.VacancyViewSet.as_view({'get': 'get_vacancies'})),
    path('vacancies/top_ten/', views.VacancyViewSet.as_view({'get': 'TopTenVacanciesAPIView'})),
    path('vacancies/<int:pk>/', views.VacancyViewSet.as_view({'get': 'get_vacancy'})),
    path('vacancies/<int:pk>/submit/', views.VacancyViewSet.as_view({'post': 'submit_vacancy'})),

    path('users/create/', views.UserViewSet.as_view({'post': 'create_user'})),

]