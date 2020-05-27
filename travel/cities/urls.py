from django.urls import path
from .views import home, CityDetailView, CityCreateView, CityUpdateView, CityDeleteView

urlpatterns = [
    path('', home, name='home'),
    path('<int:pk>/', CityDetailView.as_view(), name='current_city'),
    path('update/<int:pk>/', CityUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', CityDeleteView.as_view(), name='delete'),
    path('create/', CityCreateView.as_view(), name='create'),
]
