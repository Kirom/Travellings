from django.http import HttpResponse
from django.shortcuts import render


def home_view(request):
    return render(request, 'home.html')


def features_view(request):
    return render(request, 'features.html')
