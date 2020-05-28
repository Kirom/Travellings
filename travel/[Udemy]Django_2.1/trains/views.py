from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from .forms import TrainForm
from .models import Train


def home(request):
    trains = Train.objects.all()
    paginator = Paginator(trains, 10)
    page_number = request.GET.get('page')
    page_numbers = paginator.page_range
    page_obj = paginator.get_page(page_number)
    return render(request=request, template_name='trains/home.html',
                  context={'trains_list': trains, 'page_obj': page_obj, 'page_numbers': page_numbers})


class TrainDetailView(DetailView):
    queryset = Train.objects.all()
    template_name = 'trains/current_train.html'


class TrainCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = 'login'
    form_class = TrainForm
    model = Train
    template_name = 'trains/create.html'
    success_url = reverse_lazy('train:home')
    success_message = 'Поезд успешно создан!'

    # def post(self, request, *args, **kwargs):
    #     return super(TrainCreateView, self).post(request, *args, **kwargs)


class TrainUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    login_url = 'login'
    form_class = TrainForm
    model = Train
    template_name = 'trains/update.html'
    success_url = reverse_lazy('train:home')
    success_message = 'Поезд успешно изменен!'


class TrainDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    login_url = 'login'
    form_class = TrainForm
    model = Train
    template_name = 'trains/delete.html'
    success_url = reverse_lazy('train:home')
    success_message = 'Поезд успешно удален!'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(TrainDeleteView, self).delete(request, *args, **kwargs)
