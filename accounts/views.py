
# Create your views here.
import os
import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from accounts.models import User
from django.contrib.auth import login as django_login, logout as django_logout
from django.views import View
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index():
    return render('wa_anwa/index.html')


def kakao_login(request):
    client_id = os.environ.get('KAKAO_REST_API_KEY')
    redirect_uri = 'http://localhost:8000/accounts/signin/kakao/callback/'
    kakao_auth_api = 'https://kauth.kakao.com/oauth/authorize?'
    return redirect(f'{kakao_auth_api}client_id={client_id}&redirect_uri={redirect_uri}&response_type=code')

def kakao_callback(request):
    user = request.user
    if not user.is_authenticated:
        auth_code = request.GET.get('code')
        kakao_token_api = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': os.environ.get('KAKAO_REST_API_KEY'),
            'redirection_uri': 'http://localhost:8000/accounts/signin/kakao/callback',
            'code': auth_code
        }
        token_response = requests.post(kakao_token_api, data=data)
        access_token = token_response.json().get('access_token')
        user_info = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer ${access_token}'}).json()

        user_queryset = User.objects.filter(kakao_id=user_info['id'])
        if user_queryset.exists():  # 기존에 소셜로그인을 했었는지 확인
            user = user_queryset.first()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            django_login(request, user)
            return redirect('wa_anwa:home') #나중에 template 이름보고 수정
        else:
            user = User(
                username=user_info['properties']['nickname'],
                kakao_id=user_info['id'],
                profile_img=user_info['properties']['profile_image']
            )
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            django_login(request, user)
            return redirect('wa_anwa:home') #나중에 template 이름보고 수정

def logout(request):
    django_logout(request)
    return redirect('/')
