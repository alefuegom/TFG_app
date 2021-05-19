from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from ..models import *
from .forms import *
from .filters import *
from django.contrib.auth import logout as do_logout
from datetime import date


@login_required
def inicioTrabajador(request):
    if esTrabajador(request):
        return render(request, 'inicioTrabajador.html')
    else:
        return redirect('/errorPermiso/')

def errorPermiso(request):
        return render(request, 'errorPermisoTrabajador.html')


@login_required
def show_perfil_trabajador(request):
    if esTrabajador(request):
        persona = Persona.objects.filter(usuario=request.user)[0]
        trabajador = Trabajador.objects.filter(persona=persona)[0]
        return render(request, 'perfilTrabajador.html', {'trabajador': trabajador})
    else:
        return redirect('/errorPermiso/')


@login_required
def edit_perfil_trabajador(request):
    if esTrabajador(request):
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
                trabajador.persona.save()
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
    else:
        return redirect('/errorPermiso/')


@login_required
def list_servicios_trabajador(request):
    if esTrabajador(request):
        trabajador = Trabajador.objects.filter(persona__usuario=request.user)[0]
        servicios = Servicio.objects.filter(trabajador=trabajador)
        if len(servicios) > 0:
            servicios = servicios.order_by('-solicitudServicio__fecha')
            servicioFilter = ServicioTrabajadorFilter(request.GET, queryset=servicios)
            servicios = servicioFilter.qs
            if len(servicios) > 0:
                resultado = []
                for servicio in servicios:
                    usuario = servicio.solicitudServicio.usuario
                    try:
                        cliente = Cliente.objects.filter(persona__usuario=usuario)[0]
                        resultado.append([servicio, cliente.direccion])

                    except:
                        empresa = Empresa.objects.filter(usuario=usuario)[0]
                        resultado.append([servicio, empresa.direccion])
                paginator = Paginator(resultado, 20)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request, 'servicioTrabajador.html', {'page_obj': page_obj,
                                                                   'num_servicios': len(servicios),
                                                                   'servicioFilter': servicioFilter})
            else:
                msg_error = "No existe ningún servicio con los filtros introducidos."
                return render(request, 'servicioTrabajador.html', {'msg_error': msg_error})
        else:
            return render(request, 'servicioCliente.html')
    else:
        return redirect('/errorPermiso/')


@login_required
def show_servicios_trabajador(request, id):
    if esTrabajador(request):
        servicio = Servicio.objects.get(id=id)
        if request.user == servicio.trabajador.persona.usuario:
            try:
                empresa = Empresa.objects.filter(usuario=servicio.solicitudServicio.usuario)[0]
                return render(request, 'servicioTrabajadorForm.html', {'servicio': servicio, 'empresa': empresa})
            except:
                persona = Persona.objects.filter(usuario=servicio.solicitudServicio.usuario)[0]
                return render(request, 'servicioTrabajadorForm.html', {'servicio': servicio, 'persona': persona})
        else:
            return redirect('/errorPermiso/')
    else:
        return redirect('/errorPermiso/')


@login_required
def edit_servicio_trabajador(request, id):
    if esTrabajador(request):
        servicio = Servicio.objects.get(id=id)
        if request.user == servicio.trabajador.persona.usuario:
            if request.method == 'POST':
                form = EditServicioTrabajadorForm(request.POST, request.FILES)
                if form.is_valid():
                    if servicio.estado != 'realizado':
                        servicio.observaciones = form.cleaned_data['observaciones']
                        servicio.estado = 'realizado'
                        servicio.save()
                        creacionFactura(servicio)
                        return redirect('/trabajador/servicio/')
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
        else:
            return redirect('/errorPermiso/')
    else:
        return redirect('/errorPermiso/')


@login_required
def cerrarSesion(request):
    do_logout(request)
    response = redirect('/')
    response.delete_cookie('CK02')
    return response


def esTrabajador(request):
    return request.COOKIES.get('CK02') == "trabajador"



def creacionFactura(servicio):
    fecha_expedicion = date.today()
    emisor = "Dedesin S.L"
    usuario = servicio.solicitudServicio.usuario
    try:
        empresa = Empresa.objects.filter(usuario=usuario)[0]
        receptor = empresa.nombre
    except:
        persona = Persona.objects.filter(usuario=usuario)[0]
        receptor = persona.apellidos + ", " + persona.nombre
    descripcion = "Tratamiento para combatir  la plaga de " + servicio.solicitudServicio.plaga.nombre + \
                  ". Concretamente el tratamiento aplicado: " + servicio.solicitudServicio.tratamiento.nombre + \
                  ". Realizado el día: " + str(servicio.solicitudServicio.fecha)
    importe = servicio.solicitudServicio.tratamiento.precio
    tipo_impositivo = 21
    fecha_operaciones = fecha_expedicion

    factura = Factura(fecha_expedicion=fecha_expedicion, emisor=emisor, receptor=receptor, descripcion=descripcion,
                      importe=importe, tipo_impositivo=tipo_impositivo, fecha_operaciones=fecha_operaciones)
    factura.save()
    servicio.factura = factura
    servicio.save()
