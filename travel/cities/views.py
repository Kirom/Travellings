from django.shortcuts import render
from .models import City
from django.views.generic.detail import DetailView


def home(request):
    cities = City.objects.all()
    return render(request=request, template_name='cities/home.html', context={'cities_list': cities})


class CityDetailView(DetailView):
    queryset = City.objects.all()
    context_object_name = 'object'
    template_name = 'cities/current_city.html'
