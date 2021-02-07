from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from ..models import *
from django.contrib.auth import logout as do_logout

@login_required
def inicio_cliente(request):
    return render(request, 'inicioCliente.html')

@login_required
def solicitud_servicio_cliente(request):
    usuario = User.objects.filter(username=request.user.username)[0]
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

def logout(request):
    do_logout(request)
    return redirect('/')