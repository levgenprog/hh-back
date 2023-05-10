from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('api/vacancies/<int:pk>/submit/', consumers.VacancySubmitConsumer.as_asgi()),
]