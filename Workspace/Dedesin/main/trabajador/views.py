from django.shortcuts import render, redirect
from ..models import *
from .forms import *


def inicioTrabajador(request):
    return render(request, 'inicioTrabajador.html')


def show_perfil_trabajador(request):
    persona = Persona.objects.filter(usuario=request.user)[0]
    trabajador = Trabajador.objects.filter(persona=persona)[0]
    return render(request, 'perfilTrabajador.html', {'trabajador': trabajador})


def edit_perfil_trabajador(request):
    persona = Persona.objects.filter(usuario=request.user)[0]
    trabajador = Trabajador.objects.filter(persona=persona)[0]
    if request.method == 'POST':
        form = EditPerfilTrabajadorForm(request.POST, request.FILES)
        if form.is_valid():
            trabajador.persona.nombre = form.cleaned_data['nombre']
            trabajador.persona.apellidos = form.cleaned_data['apellidos']
            trabajador.persona.telefono = form.cleaned_data['telefono']
            trabajador.cualificacion = form.cleaned_data['cualificacion']
            trabajador.persona.dni = form.cleaned_data['dni']
            trabajador.save()
            return redirect('/trabajador/miPerfil')
        else:
            valores = [trabajador.persona.nombre, trabajador.persona.apellidos, trabajador.persona.dni,
                       trabajador.persona.telefono, trabajador.cualificacion]
            items = zip(form, valores)
            return render(request, 'perfilTrabajador.html', {'form': form, 'items': items})

    else:
        form = EditPerfilTrabajadorForm()
        valores = [trabajador.persona.nombre, trabajador.persona.apellidos, trabajador.persona.dni,
                   trabajador.persona.telefono, trabajador.cualificacion]
        items = zip(form, valores)
        return render(request, 'perfilTrabajador.html', {'form': form, 'items': items})


def list_servicios_trabajador(request):
    persona = Persona.objects.filter(usuario=request.user)[0]
    trabajador = Trabajador.objects.filter(persona=persona)[0]
    servicios = Servicio.objects.filter(trabajador=trabajador)
    return render(request, 'servicioTrabajador.html', {'servicios': servicios, 'num_servicios': len(servicios)})


def show_servicios_trabajador(request, id):
    servicio = Servicio.objects.get(id=id)
    try:
        empresa = Empresa.objects.filter(usuario=servicio.solicitudServicio.usuario)[0]
        return render(request, 'servicioTrabajadorForm.html', {'servicio': servicio, 'empresa': empresa})
    except:
        persona = Persona.objects.filter(usuario=servicio.solicitudServicio.usuario)[0]
        return render(request, 'servicioTrabajadorForm.html', {'servicio': servicio, 'persona': persona})


def edit_servicio_trabajador(request, id):
    servicio = Servicio.objects.get(id=id)
    if request.method == 'POST':
        form = EditServicioTrabajadorForm(request.POST, request.FILES)
        if form.is_valid():
            print(servicio.estado)
            if servicio.estado != 'realizado':
                servicio.observaciones = form.cleaned_data['observaciones']
                servicio.estado = 'realizado'
                servicio.save()
                return redirect('/trabajador/servicios/')
            else:
                msg_error = 'No se puede editar un servicio que ya ha sido realizado.'
                try:
                    empresa = Empresa.objects.filter(usuario=servicio.solicitudServicio.usuario)[0]
                    return render(request, 'servicioTrabajadorForm.html', {'form': form, 'servicio': servicio
                        , 'empresa': empresa, 'msg_error': msg_error})
                except:
                    persona = Persona.objects.filter(usuario=servicio.solicitudServicio.usuario)[0]
                    return render(request, 'servicioTrabajadorForm.html',
                                  {'form': form, 'servicio': servicio, 'msg_error': msg_error,
                                   'persona': persona})
        else:
            try:
                empresa = Empresa.objects.filter(usuario=servicio.solicitudServicio.usuario)[0]
                return render(request, 'servicioTrabajadorForm.html', {'form': form, 'servicio_edit': servicio
                    , 'empresa': empresa})
            except:
                persona = Persona.objects.filter(usuario=servicio.solicitudServicio.usuario)[0]
                return render(request, 'servicioTrabajadorForm.html',
                              {'form': form, 'servicio_edit': servicio, 'persona': persona})
    else:
        form = EditServicioTrabajadorForm()
        if servicio.estado != 'realizado':
            try:
                empresa = Empresa.objects.filter(usuario=servicio.solicitudServicio.usuario)[0]
                return render(request, 'servicioTrabajadorForm.html', {'form': form, 'servicio_edit': servicio
                    , 'empresa': empresa})
            except:
                persona = Persona.objects.filter(usuario=servicio.solicitudServicio.usuario)[0]
                return render(request, 'servicioTrabajadorForm.html', {'form': form, 'servicio_edit': servicio,
                                                                       'persona': persona})
        else:
            msg_error = 'No se puede editar un servicio que ya ha sido realizado.'
            try:
                empresa = Empresa.objects.filter(usuario=servicio.solicitudServicio.usuario)[0]
                return render(request, 'servicioTrabajadorForm.html', {'form': form, 'servicio': servicio
                    , 'empresa': empresa, 'msg_error': msg_error})
            except:
                persona = Persona.objects.filter(usuario=servicio.solicitudServicio.usuario)[0]
                return render(request, 'servicioTrabajadorForm.html',
                              {'form': form, 'servicio': servicio, 'msg_error': msg_error,
                               'persona': persona})
