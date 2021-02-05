from django.shortcuts import render

# Create your views here.
from ..models import *


def inicio_cliente(request):
    return render(request, 'inicioCliente.html')


def solicitud_servicio_cliente(request):
    usuario = Usuario.objects.get(email="cliente1@cliente.com")
    solicitudes = SolicitudServicio.objects.filter(usuario=usuario)
    if solicitudes:
        return render(request, 'solicitudServicioCliente.html', {'solicitudes': solicitudes,
                                                                 'num_solicitudes': solicitudes.count()})
    else:
        return render(request, 'solicitudServicioCliente.html')


def servicio_cliente(request):
    return render(request, 'servicioCliente.html')


def perfil_cliente(request):
    return render(request, 'perfilCliente.html')


def solicitud_servicio_cliente_form(request):
    return render(request, 'solicitudServicioClienteForm.html')


def solicitud_servicio_cliente_form(request):
    return render(request, 'servicioClienteForm.html')
