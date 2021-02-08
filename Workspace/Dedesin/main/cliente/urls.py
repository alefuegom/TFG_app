"""Dedesin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from . import views

urlpatterns = [
    path('', views.inicio_cliente),
    path('solicitudServicio/', views.list_solicitud_servicio_cliente),
    path('solicitudServicio/show/<int:id>/', views.show_solicitud_servicio_cliente),
    path('solicitudServicio/edit/<int:id>/', views.edit_solicitud_servicio_cliente),
    path('solicitudServicio/create/', views.create_solicitud_servicio_cliente),
    path('servicio/', views.servicio_cliente),
    path('miPerfil/', views.perfil_cliente),
    path('cerrarSesion/', views.logout)
]
