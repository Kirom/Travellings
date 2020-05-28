from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .models import City
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import CityForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


def home(request):
    cities = City.objects.all()
    paginator = Paginator(cities, 5)
    page_number = request.GET.get('page')
    page_numbers = paginator.page_range
    page_obj = paginator.get_page(page_number)
    return render(request=request, template_name='cities/home.html',
                  context={'cities_list': cities, 'page_obj': page_obj, 'page_numbers': page_numbers})


class CityDetailView(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/current_city.html'


class CityCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = CityForm
    model = City
    template_name = 'cities/create.html'
    success_url = reverse_lazy('city:home')
    success_message = 'Город успешно создан!'


class CityUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = CityForm
    model = City
    template_name = 'cities/update.html'
    success_url = reverse_lazy('city:home')
    success_message = 'Город успешно изменен!'


class CityDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    # form_class = CityForm
    login_url = '/login/'
    model = City
    template_name = 'cities/delete.html'
    success_url = reverse_lazy('city:home')
    success_message = 'Город успешно удален!'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(CityDeleteView, self).delete(request, *args, **kwargs)
