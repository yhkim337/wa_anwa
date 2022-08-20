from django.urls import path
from wa_anwa import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('weather_api', views.weather_api, name='weather_api')
]