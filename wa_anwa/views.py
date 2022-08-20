from django.shortcuts import render

# Create your views here.
def home(request):
    user = request.user
    if user.is_authenticated:
         return render(request, 'wa_anwa/home.html')
    else:
        return render(request, 'wa_anwa/index.html')

