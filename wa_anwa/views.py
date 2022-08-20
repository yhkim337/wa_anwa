from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'wa_anwa/index.html')

def home(request):
    user = request.user
    if user.is_authenticated:
         return render(request, 'wa_anwa/home.html')
    else:
        return render(request, 'wa_anwa/index.html')
   