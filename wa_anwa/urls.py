from django.urls import path
from wa_anwa import views
from django.conf.urls.static import static
from django.conf import settings

app_name='wa_anwa'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('betting/<int:id>/', views.betting, name='betting'),
    path('', views.map, name='map'),
    path('time/', views.time, name='time'),
    path('createparticipate/', views.createparticipate, name="createparticipate"),
    path('ranking/', views.ranking, name = "ranking"),
    path('mypage/', views.my_page, name='mypage'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)