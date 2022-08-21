from django.urls import path
from wa_anwa import views

app_name='wa_anwa'

urlpatterns = [

    path('index/', views.index, name='index'),
    path('betting/<int:id>/', views.betting, name='betting'),
    path('', views.map, name='map'),
    path('time/', views.time, name='time'),
    path('createparticipate/', views.createparticipate, name="createparticipate"),
    path('ranking/', views.ranking, name = "ranking"),
    path('mypage/', views.my_page, name='mypage'),

    path('get_answer', views.get_answer, name='get_answer'),
    path('set_answer', views.set_answer, name='set_answer')
]
