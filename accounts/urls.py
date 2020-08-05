from django.urls import path

from accounts.views import logout_view, registration_view, UserPasswordResetView, UserLoginView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('registration/', registration_view, name='registration'),
    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
]
