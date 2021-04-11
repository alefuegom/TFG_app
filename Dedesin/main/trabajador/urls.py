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
    path('', views.inicioTrabajador),
    path('servicios/', views.list_servicios_trabajador),
    path('servicios/show/<int:id>/', views.show_servicios_trabajador),
    path('servicios/edit/<int:id>/', views.edit_servicio_trabajador),
    path('miPerfil/', views.show_perfil_trabajador),
    path('miPerfil/edit/', views.edit_perfil_trabajador),
    path('cerrarSesion', views.cerrarSesion)

]


