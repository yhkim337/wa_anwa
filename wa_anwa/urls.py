from django.urls import path
from wa_anwa import views

app_name='wa_anwa'

urlpatterns = [
    path('index/', views.index, name='index'), 
    path('map/', views.map, name='map'),
    path('betting/', views.betting, name='betting'),
    path('', views.home, name='home'),
]