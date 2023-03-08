from django.shortcuts import render, HttpResponse

# Create your views here.


def home_index(request):
    return render(request, 'home/index.html')
