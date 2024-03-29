from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import *
from datetime import datetime, date
from ..models import *
from django.contrib.auth import logout as do_logout
from .filters import *


# VISTAS GENERALES
@login_required
def inicio_cliente(request):
    if esCliente(request):
        nombre_cliente = Cliente.objects.get(
            persona__usuario=request.user).nombreCompleto()
        return render(request, 'inicioCliente.html', {'nombre_cliente': nombre_cliente})
    else:
        return redirect('/errorPermiso/')


@login_required
def show_perfil_cliente(request):
    if esCliente(request):
        persona = Persona.objects.filter(usuario=request.user)[0]
        cliente = Cliente.objects.filter(persona=persona)[0]
        return render(request, 'perfilCliente.html', {'cliente': cliente})
    else:
        return redirect('/errorPermiso')


@login_required
def edit_perfil_cliente(request):
    if esCliente(request):
        persona = Persona.objects.filter(usuario=request.user)[0]
        cliente = Cliente.objects.filter(persona=persona)[0]
        if request.method == 'POST':
            form = EditPerfilClienteForm(request.POST, request.FILES)
            if form.is_valid():
                persona = Persona.objects.filter(usuario=request.user)[0]
                cliente = Cliente.objects.filter(persona=persona)[0]
                persona.nombre = form.cleaned_data['nombre']
                persona.apellidos = form.cleaned_data['apellidos']
                persona.dni = form.cleaned_data['dni']
                persona.telefono = form.cleaned_data['telefono']
                cliente.direccion = form.cleaned_data['direccion']
                cliente.cuenta_bancaria = form.cleaned_data['cuentaBancaria']
                persona.save()
                cliente.save()
                return redirect('/cliente/miPerfil')
            else:
                cuenta_bancaria = cliente.cuenta_bancaria
                if not cuenta_bancaria:
                    cuenta_bancaria = ""
                valores = [persona.nombre, persona.apellidos, persona.dni, persona.telefono, cliente.direccion,
                           cuenta_bancaria]
                items = zip(form, valores)
                return render(request, 'perfilCliente.html', {'form': form, 'items': items})
        else:
            form = EditPerfilClienteForm()
            cuenta_bancaria = cliente.cuenta_bancaria
            if not cuenta_bancaria:
                cuenta_bancaria = ""
            valores = [persona.nombre, persona.apellidos, persona.dni, persona.telefono, cliente.direccion,
                       cuenta_bancaria]
            items = zip(form, valores)
            return render(request, 'perfilCliente.html', {'form': form, 'items': items})
    else:
        return redirect('/errorPermiso')


def errorPermiso(request):
    return render(request, 'errorPermisoCliente.html')


def politicaPrivacidad(request):
    return render(request, 'politicaPrivacidadCliente.html')

# CRUD SERVICIOS


@login_required
def list_servicios_cliente(request):
    if esCliente(request):
        usuario = User.objects.filter(username=request.user.username)[0]
        servicios = Servicio.objects.filter(solicitudServicio__usuario=usuario)
        if len(servicios) > 0:
            servicios = servicios.order_by('-solicitudServicio__fecha')
            servicioFilter = ServicioClienteFilter(
                request.GET, queryset=servicios)
            servicios = servicioFilter.qs
            if len(servicios) > 0:
                paginator = Paginator(servicios, 10)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request, 'servicioCliente.html', {'page_obj': page_obj,
                                                                'num_servicios': len(servicios),
                                                                'servicioFilter': servicioFilter})
            else:
                msg_error = "No existe ningún servicio con los filtros introducidos."
                return render(request, 'servicioCliente.html', {'msg_error': msg_error})
        else:
            return render(request, 'servicioCliente.html')
    else:
        return redirect('/errorPermiso')


@login_required
def show_servicios_cliente(request, id):
    if esCliente(request):
        servicio = Servicio.objects.get(id=id)
        if servicio:
            if request.user == servicio.solicitudServicio.usuario:
                return render(request, 'servicioClienteForm.html', {'servicio': servicio})
            else:
                return redirect('/errorPermiso')
        else:
            return render(request, 'servicioClienteForm.html')
    else:
        return redirect('/errorPermiso')


# CRUD SOLICITUD DE SERVICIO
@login_required
def list_solicitud_servicio_cliente(request):
    if esCliente(request):
        servicios = Servicio.objects.filter(
            estado="Pendiente", solicitudServicio__usuario=request.user)
        list_ids = []
        if len(servicios) > 0:
            for servicio in servicios:
                list_ids.append(servicio.solicitudServicio.id)
        solicitudes = SolicitudServicio.objects.filter(Q(estado="Pendiente") | Q(
            estado="Atendida") | Q(estado="Rechazada" ) | Q(id__in=list_ids) , usuario=request.user)
        if len(solicitudes) > 0:
            solicitudServicioFilter = SolicitudServicioClienteFilter(
                request.GET, queryset=solicitudes)
            solicitudes = solicitudServicioFilter.qs
            if len(solicitudes) > 0:
                solicitudes = solicitudes.order_by('-fecha')
                paginator = Paginator(solicitudes, 10)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request, 'solicitudServicioCliente.html', {'page_obj': page_obj,
                                                                         'num_solicitudes': solicitudes.count(),
                                                                         'solicitudServicioFilter': solicitudServicioFilter})
            else:
                msg_error = "No existe ninguna solicitud de servicio con los filtros introducidos."
                return render(request, 'solicitudServicioCliente.html', {'msg_error': msg_error})
        else:
            return render(request, 'solicitudServicioCliente.html')
    else:
        return redirect('/errorPermiso')


@login_required
def create_solicitud_servicio_cliente(request):
    if esCliente(request):
        if request.method == 'POST':
            form = CreateSolicitudServicioClienteForm(
                request.POST, request.FILES)
            if form.is_valid():
                usuario = request.user
                estado = 'Pendiente'
                fecha = None
                tratamiento = None
                nombre_plaga = form.cleaned_data['plaga']
                plaga = Plaga.objects.filter(nombre=nombre_plaga)[0]
                observaciones = form.cleaned_data['observaciones']
                solicitud = SolicitudServicio(usuario=usuario, estado=estado, fecha=fecha, tratamiento=tratamiento,
                                              plaga=plaga,
                                              observaciones=observaciones)
                solicitud.save()
                return redirect("/cliente/solicitudServicio/")
        else:
            form = CreateSolicitudServicioClienteForm()
            return render(request, 'createSolicitudServicioCliente.html', {'form': form})
    else:
        return redirect('/errorPermiso')


@login_required
def show_solicitud_servicio_cliente(request, id):
    if esCliente(request):
        solicitud = SolicitudServicio.objects.get(id=id)
        if request.user == solicitud.usuario:
            return render(request, 'solicitudServicioClienteForm.html', {'solicitud': solicitud})
        else:
            return redirect('/errorPermiso')
    else:
        return redirect('/errorPermiso')


@login_required
def edit_solicitud_servicio_cliente(request, id):
    print(request.user)
    if esCliente(request):
        solicitud = SolicitudServicio.objects.get(id=id)
        if request.user == solicitud.usuario:
            if solicitud.estado == 'Pendiente':
                if request.method == 'POST':
                    form = EditSolicitudServicioPendienteClienteForm(
                        request.POST, request.FILES)
                    if form.is_valid():
                        plaga = form.cleaned_data['plaga']
                        observaciones = form.cleaned_data['observaciones']
                        solicitud.plaga = Plaga.objects.get(nombre=plaga)
                        solicitud.observaciones = observaciones
                        solicitud.save()
                        return redirect("/cliente/solicitudServicio/show/" + str(solicitud.id))
                else:
                    form = EditSolicitudServicioPendienteClienteForm()
                    values = [solicitud.plaga, solicitud.observaciones]
                    items = zip(form, values)
                    return render(request, 'solicitudServicioClienteForm.html', {'solicitud': solicitud, 'items': items})
            if solicitud.estado == 'Atendida':
                if request.method == 'POST':
                    form = EditSolicitudServicioClienteForm(
                        request.POST, request.FILES)
                    if form.is_valid():
                        estado = form.cleaned_data['estado']
                        solicitud.estado = estado
                        solicitud.save()
                        if estado == 'Rechazada':
                            return redirect("/cliente/solicitudServicio/show/" + str(solicitud.id))
                        elif estado == 'Aceptada':
                            servicio = Servicio(
                                solicitudServicio=solicitud, estado="Pendiente")
                            servicio.save()
                            return redirect("/cliente/servicio/show/" + str(servicio.id))
                else:
                    form = EditSolicitudServicioClienteForm()
                    return render(request, 'solicitudServicioClienteForm.html', {'solicitud': solicitud, 'form': form})
            else:
                msg_error = "Exclusivamente se puede editar una solicitud de servicio si su estado es 'Atendida'"
                return render(request, 'solicitudServicioClienteForm.html', {'solicitud': solicitud,
                                                                             'msg_error': msg_error})
        else:
            return redirect('/errorPermiso')
    else:
        return redirect('/errorPermiso')


@login_required()
def show_factura_cliente(request, id):
    if esCliente(request):
        servicio = Servicio.objects.get(id=id)
        factura = servicio.factura
        return render(request, 'facturaClienteForm.html', {'servicio': servicio, 'factura': factura})
    else:
        return redirect("/errorPermiso/")


def logout(request):
    do_logout(request)
    response = redirect('/')
    response.delete_cookie('CK02')
    return response


def esCliente(request):
    esCliente = request.COOKIES.get('CK02') == "cliente"
    return esCliente
