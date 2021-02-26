from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from django.contrib.auth import logout as do_logout

from .forms import *
from ..models import *


@login_required
def inicioAdministrador(request):
    if esAdministrador(request):
        return render(request, 'inicioAdministrador.html')
    else:
        return redirect('/errorPermiso/')


@login_required
def show_perfil_administrador(request):
    if esAdministrador(request):
        persona = Persona.objects.filter(usuario=request.user)[0]
        administrador = Administrador.objects.filter(persona=persona)[0]
        return render(request, 'perfilAdministrador.html', {'administrador': administrador})
    else:
        return redirect('/errorPermiso/')


@login_required
def edit_perfil_administrador(request):
    if esAdministrador(request):
        persona = Persona.objects.filter(usuario=request.user)[0]
        if request.method == 'POST':
            form = EditPerfilAdministrador(request.POST, request.FILES)
            if form.is_valid():
                persona.dni = form.cleaned_data['dni']
                persona.nombre = form.cleaned_data['nombre']
                persona.apellidos = form.cleaned_data['apellidos']
                persona.telefono = form.cleaned_data['telefono']
                persona.usuario.username = form.cleaned_data['email']
                persona.usuario.save()
                persona.save()
                return redirect('/administrador/miPerfil/')
            else:
                valores = [persona.nombre, persona.apellidos, persona.usuario.username, persona.dni, persona.telefono]
                items = zip(form, valores)
                return render(request, 'perfilAdministrador.html', {'form': form, 'items': items})
        else:
            form = EditPerfilAdministrador()
            valores = [persona.nombre, persona.apellidos, persona.usuario.email, persona.dni, persona.telefono]
            items = zip(form, valores)
            return render(request, 'perfilAdministrador.html', {'form': form, 'items': items})
    else:
        return redirect('/errorPermiso/')


@login_required
def list_solicitudServicio_administrador(request):
    if esAdministrador(request):
        solicitudes = SolicitudServicio.objects.all()
        return render(request, 'solicitudServicioAdministrador.html', {'solicitudes': solicitudes, 'num_solicitudes':
            len(solicitudes)})
    else:
        return redirect('/errorPermiso/')


@login_required
def show_solicitudServicio_administrador(request, id):
    if esAdministrador(request):
        solicitud = SolicitudServicio.objects.get(id=id)
        try:
            empresa = Empresa.objects.filter(usuario=solicitud.usuario)[0]
            return render(request, 'solicitudServicioAdministradorForm.html',
                          {'solicitud': solicitud, 'empresa': empresa})
        except:
            persona = Persona.objects.filter(usuario=solicitud.usuario)[0]
            cliente = Cliente.objects.filter(persona=persona)[0]
            return render(request, 'solicitudServicioAdministradorForm.html',
                          {'solicitud': solicitud, 'cliente': cliente})
    else:
        return redirect('/errorPermiso/')


@login_required
def edit_solicitudServicio_administrador(request, id):
    if esAdministrador(request):
        solicitud = SolicitudServicio.objects.get(id=id)
        if solicitud.estado == 'Pendiente':
            if request.method == 'POST':
                form = EditSolicitudServicioAdministradorForm(request.POST, request.FILES)
                if form.is_valid():
                    try:
                        fecha_str = form.cleaned_data['fecha']
                        solicitud.fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date()
                        if solicitud.fecha <= date.today():
                            msg_error = "La fecha debe ser posterior a la fecha actual."
                            return render(request, 'solicitudServicioAdministradorForm.html',
                                          {'form': form, 'solicitud_edit': solicitud,
                                           'msg_error': msg_error})
                        solicitud.tratamiento = Tratamiento.objects.get(id=form.cleaned_data['tratamiento'])
                        if solicitud.tratamiento.plaga != solicitud.plaga:
                            msg_error = "La plaga que combate el tratamiento debe ser igual a la plaga introducida en la solicitud de servicio."
                            return render(request, 'solicitudServicioAdministradorForm.html',
                                          {'form': form, 'solicitud_edit': solicitud,
                                           'msg_error': msg_error})
                        solicitud.estado = 'Atendida'
                        solicitud.save()
                        return redirect('/administrador/solicitudServicio/')
                    except:
                        msg_error = "Introduzca un formato de fecha correcto (dd/mm/yyyy)"
                        return render(request, 'solicitudServicioAdministradorForm.html',
                                      {'form': form, 'solicitud_edit': solicitud,
                                       'msg_error': msg_error})
                else:
                    return render(request, 'solicitudServicioAdministradorForm.html',
                                  {'solicitud_edit': solicitud, 'form': form})
            else:
                form = EditSolicitudServicioAdministradorForm()
                return render(request, 'solicitudServicioAdministradorForm.html',
                              {'solicitud_edit': solicitud, 'form': form})
        else:
            msg_error = 'Exclusivamente se puede editar una solicitud de servicio ' \
                        'si su estado tiene el valor de "Pendiente".'
            return render(request, 'solicitudServicioAdministradorForm.html',
                          {'solicitud': solicitud, 'msg_error': msg_error})
    else:
        return redirect('/errorPermiso/')


@login_required
def list_servicio_administrador(request):
    if esAdministrador(request):
        servicios = Servicio.objects.all()
        return render(request, 'servicioAdministrador.html', {'servicios': servicios, 'num_servicios': len(servicios)})
    else:
        return redirect('/errorPermiso/')


@login_required
def show_servicio_administrador(request, id):
    if esAdministrador(request):
        servicio = Servicio.objects.get(id=id)
        try:
            empresa = Empresa.objects.filter(usuario=servicio.solicitudServicio.usuario)[0]
            return render(request, 'servicioAdministradorForm.html', {'servicio': servicio, 'empresa': empresa})
        except:
            persona = Persona.objects.filter(usuario=servicio.solicitudServicio.usuario)[0]
            cliente = Cliente.objects.filter(persona=persona)[0]
            return render(request, 'servicioAdministradorForm.html', {'servicio': servicio, 'cliente': cliente})
    else:
        return redirect('/errorPermiso/')


@login_required
def edit_servicio_administrador(request, id):
    if esAdministrador(request):
        servicio = Servicio.objects.get(id=id)
        if servicio.estado == "Pendiente":
            if request.method == 'POST':
                form = EditServicioAdministradorForm(request.POST, request.FILES)
                if form.is_valid():
                    servicio.trabajador = Trabajador.objects.get(id=form.cleaned_data['trabajador'])
                    servicio.save()
                    return redirect('/administrador/servicio/')
            else:
                form = EditServicioAdministradorForm()
                return render(request, 'servicioAdministradorForm.html', {'servicio_edit': servicio,
                                                                          'form': form})
        else:
            msg_error = 'Exclusivamente se puede editar un servicio ' \
                        'si su estado tiene el valor de "Pendiente".'
            return render(request, 'servicioAdministradorForm.html', {'servicio': servicio, 'msg_error': msg_error})
    else:
        return redirect('/errorPermiso/')


@login_required
def cerrarSesion(request):
    do_logout(request)
    return redirect('/')


def esAdministrador(request):
    try:
        persona = Persona.objects.filter(usuario=request.user)[0]
        administrador = Administrador.objects.filter(persona=persona)[0]
        return administrador
    except:
        return None
