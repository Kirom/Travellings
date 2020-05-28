from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

# from .forms import UserLoginForm
from django.views.generic import FormView

from travel.forms import UserLoginForm, UserRegistrationForm


def home(request):
    return render(request, 'home.html')


def login_view(request):
    form = UserLoginForm(request.POST or None)
    next_ = request.GET.get('next')
    if form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username.strip(), password=password.strip())
        login(request, user)
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or '/'
        return redirect(redirect_path)
    return render(request, 'login.html', context={'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def registration_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': user_form})

# class RegistrationView(FormView):
#     form_class = UserRegistrationForm
#     success_url = "/login/"
#     template_name = 'registration.html'
#
#     def form_valid(self, form):
#         form.save()
#         # Функция super( тип [ , объект или тип ] )
#         # Возвратите объект прокси, который делегирует вызовы метода родительскому или родственному классу типа .
#         return super(RegistrationView, self).form_valid(form)
#
#     def form_invalid(self, form):
#         return super(RegistrationView, self).form_invalid(form)
