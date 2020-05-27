from django.urls import path
from .views import home, TrainCreateView, TrainDeleteView, TrainUpdateView, TrainDetailView

urlpatterns = [
    path('', home, name='home'),
    path('<int:pk>/', TrainDetailView.as_view(), name='current_train'),
    path('update/<int:pk>/', TrainUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', TrainDeleteView.as_view(), name='delete'),
    path('create/', TrainCreateView.as_view(), name='create'),
]
