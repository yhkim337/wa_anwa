"""hackathon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
import wa_anwa.views
import accounts.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', wa_anwa.views.home, name='home'),
    path('wa_anwa/', include('wa_anwa.urls', namespace="wa_anwa")), 
    path('accounts/', include('accounts.urls', namespace="accounts")),
    path('accounts/kakao-login/', accounts.views.kakao_login, name='kakao-login'),
    path('accounts/signin/kakao/callback/', accounts.views.kakao_callback, name='kakao-callback'),
    path('social_accounts/', include('allauth.urls')),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
