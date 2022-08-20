from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'wa_anwa/index.html')

def weather_api(request):
    return render(request, 'weather_api.html')
    