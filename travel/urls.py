"""travel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from routes.views import home, find_routes, add_route, RouteDeleteView, RouteListView, RouteDetailView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('cities/', include(('cities.urls', 'city'))),
    path('accounts/', include(('accounts.urls', 'accounts'))),
    path('trains/', include(('trains.urls', 'train'))),
    path('add_route/', add_route, name='add_route'),
    path('find/', find_routes, name='find_routes'),
    path('routes/', RouteListView.as_view(), name='routes'),
    path('routes/<int:pk>/', RouteDetailView.as_view(), name='current_route'),
    path('routes/delete/<int:pk>/', RouteDeleteView.as_view(), name='delete_route'),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
