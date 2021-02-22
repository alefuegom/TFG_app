from django.shortcuts import *
from django.contrib.auth import logout as do_logout

from ..models import *


def inicioAdministrador(request):
    return render(request, 'inicioAdministrador.html')


def list_solicitudServicio_administrador(request):
    solicitudes = SolicitudServicio.objects.all()
    return render(request, 'solicitudServicioAdministrador.html', {'solicitudes': solicitudes, 'num_solicitudes':
        len(solicitudes)})


def show_solicitudServicio_administrador(request, id):
    solicitud = SolicitudServicio.objects.get(id=id)
    try:
        empresa = Empresa.objects.filter(usuario=solicitud.usuario)[0]
        return render(request, 'solicitudServicioAdministradorForm.html', {'solicitud': solicitud, 'empresa': empresa})
    except:
        persona = Persona.objects.filter(usuario=solicitud.usuario)[0]
        cliente = Cliente.objects.filter(persona=persona)[0]
        return render(request, 'solicitudServicioAdministradorForm.html', {'solicitud': solicitud, 'cliente': cliente})


def list_servicio_administrador(request):
    servicios = Servicio.objects.all()
    return render(request, 'servicioAdministrador.html', {'servicios': servicios, 'num_servicios': len(servicios)})


def show_servicio_administrador(request, id):
    servicio = Servicio.objects.get(id=id)
    try:
        empresa = Empresa.objects.filter(usuario=servicio.solicitudServicio.usuario)[0]
        return render(request, 'servicioAdministradorForm.html', {'servicio': servicio, 'empresa': empresa})
    except:
        persona = Persona.objects.filter(usuario=servicio.solicitudServicio.usuario)[0]
        cliente = Cliente.objects.filter(persona=persona)[0]
        return render(request, 'servicioAdministradorForm.html', {'servicio': servicio, 'cliente': cliente})


def cerrarSesion(request):
    do_logout(request)
    return redirect('/')
