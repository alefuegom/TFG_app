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
    path('', views.inicioAdministrador),
    path('cerrarSesion/', views.cerrarSesion),
    path('solicitudServicio/', views.list_solicitudServicio_administrador),
    path('solicitudServicio/show/<int:id>/', views.show_solicitudServicio_administrador),
    path('solicitudServicio/edit/<int:id>/', views.edit_solicitudServicio_administrador),
    path('servicio/', views.list_servicio_administrador),
    path('servicio/show/<int:id>/', views.show_servicio_administrador),
    path('servicio/edit/<int:id>/', views.edit_servicio_administrador),
    path('miPerfil/', views.show_perfil_administrador),
    path('miPerfil/edit/', views.edit_perfil_administrador),
    path('plaga/', views.list_plaga_administrador),
    path('plaga/delete/<int:id>/', views.delete_plaga_administrador),
    path('plaga/create/', views.create_plaga_administrador),
    path('tratamiento/', views.list_tratamiento_administrador),
    path('tratamiento/show/<int:id>/', views.show_tratamiento_administrador),
    path('tratamiento/create/', views.create_tratamiento_administrador),
    path('tratamiento/edit/<int:id>/', views.edit_tratamiento_administrador),
    path('tratamiento/delete/<int:id>/', views.delete_tratamiento_administrador),
    path('factura/', views.list_facturas_administrador),
    path('factura/show/<int:id>/', views.show_factura_administrador),
    path('vehiculo/', views.list_vehiculo_administrador),
    path('vehiculo/show/<int:id>/', views.show_vehiculo_administrador),
    path('vehiculo/create/', views.create_vehiculo_administrador),
    path('vehiculo/edit/<int:id>/', views.edit_vehiculo_administrador),
    path('vehiculo/delete/<int:id>/', views.delete_vehiculo_administrador),
    path('trabajador/', views.list_trabajador_administrador),
    path('trabajador/show/<int:id>/', views.show_trabajador_administrador),
    path('trabajador/create/', views.create_trabajador_administrador),
    path('trabajador/edit/<int:id>/', views.edit_trabajador_administrador),
    path('trabajador/delete/<int:id>/', views.delete_trabajador_administrador),
    path('cliente/', views.list_cliente_administrador),
    path('cliente/show/<int:id>/', views.show_cliente_administrador),
    path('empresa/', views.list_empresa_administrador),
    path('empresa/show/<int:id>/', views.show_empresa_administrador),
    path('administrador/', views.list_administrador_administrador),
    path('administrador/show/<int:id>/', views.show_administrador_administrador),
    path('administrador/create/', views.create_administrador_administrador),
    path('administrador/edit/<int:id>/', views.edit_administrador_administrador),
    path('administrador/delete/<int:id>/', views.delete_administrador_administrador),
    path('panelControl/', views.show_panelControl_administrador)

]
