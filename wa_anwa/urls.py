from django.urls import path
from wa_anwa import views

urlpatterns = [
    path('', views.index, name='index'), 
]