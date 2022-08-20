from django.urls import path
from wa_anwa import views

app_name='wa_anwa'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.map, name='map'),
    path('time/', views.time, name='time'),
    path('createparticipate/', views.createparticipate, name="createparticipate"),
]