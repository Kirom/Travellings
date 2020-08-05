from django.urls import path

from accounts.views import login_view, logout_view, registration_view, password_reset_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registration/', registration_view, name='registration'),
    path('password_reset/', password_reset_view, name='password_reset'),
]
