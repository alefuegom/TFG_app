from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .forms import *
from ..models import *
from .filters import *
from django.contrib.auth import logout as do_logout


# MÉTODOS AUXILIARES
def esEmpresa(request):
    try:
        empresa = Empresa.objects.filter(usuario=request.user)[0]
        return empresa
    except:
        return None


# VISTAS GENERALES
@login_required
def inicio_empresa(request):
    if esEmpresa(request):
        return render(request, 'inicioEmpresa.html')
    else:
        return redirect('/errorPermiso/')


@login_required
def show_perfil_empresa(request):
    if esEmpresa(request):
        empresa = Empresa.objects.filter(usuario=request.user)[0]
        return render(request, 'perfilEmpresa.html', {'empresa': empresa})
    else:
        return redirect('/errorPermiso/')


@login_required
def edit_perfil_empresa(request):
    if esEmpresa(request):
        empresa = Empresa.objects.filter(usuario=request.user)[0]
        if request.method == 'POST':
            form = EditPerfilEmpresaForm(request.POST, request.FILES)
            if form.is_valid():
                empresa.nombre = form.cleaned_data['nombre']
                empresa.cif = form.cleaned_data['cif']
                empresa.telefono = form.cleaned_data['telefono']
                empresa.direccion = form.cleaned_data['direccion']
                empresa.cuenta_bancaria = form.cleaned_data['cuentaBancaria']
                empresa.save()
                return redirect('/empresa/miPerfil')
            else:
                valores = [empresa.nombre, empresa.cif, empresa.telefono, empresa.direccion,
                           empresa.cuenta_bancaria]
                items = zip(form, valores)
                msg_error = "No se ha completado correctamente alguno de los campos. Por favor, vuelva a intentarlo."
                return render(request, 'perfilEmpresa.html', {'form': form, 'items': items, 'msg_error': msg_error})

        else:
            form = EditPerfilEmpresaForm()
            valores = [empresa.nombre, empresa.cif, empresa.telefono, empresa.direccion,
                       empresa.cuenta_bancaria]
            items = zip(form, valores)
            return render(request, 'perfilEmpresa.html', {'form': form, 'items': items})
    else:
        return redirect('/errorPermiso/')


def logout(request):
    do_logout(request)
    return redirect('/')


# CRUD SERVICIOS
@login_required
def list_servicios_empresa(request):
    if esEmpresa(request):
        usuario = User.objects.filter(username=request.user.username)[0]
        servicios = Servicio.objects.filter(solicitudServicio__usuario=usuario)
        if len(servicios) > 0:
            servicios = servicios.order_by('-solicitudServicio__fecha')
            servicioFilter = ServicioEmpresaFilter(request.GET, queryset=servicios)
            servicios = servicioFilter.qs
            if len(servicios) > 0:
                paginator = Paginator(servicios, 10)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request, 'servicioEmpresa.html', {'page_obj': page_obj,
                                                                'num_servicios': len(servicios),
                                                                'servicioFilter': servicioFilter})
            else:
                msg_error = "No existe ningún servicio con los filtros introducidos."
                return render(request, 'servicioEmpresa.html', {'msg_error': msg_error})
        else:
            return render(request, 'servicioCliente.html')
    else:
        return redirect('/errorPermiso/')


@login_required
def show_servicios_empresa(request, id):
    if esEmpresa(request):
        servicio = Servicio.objects.get(id=id)
        if servicio:
            if request.user == servicio.solicitudServicio.usuario:
                return render(request, 'servicioEmpresaForm.html', {'servicio': servicio})
            else:
                return redirect('/errorPermiso')
        else:
            return render(request, 'servicioEmpresaForm.html')
    else:
        return redirect('/errorPermiso/')


# CRUD SOLICITUD DE SERVICIO
@login_required
def list_solicitud_servicio_empresa(request):
    if esEmpresa(request):
        usuario = User.objects.filter(username=request.user.username)[0]
        solicitudes = SolicitudServicio.objects.filter(usuario=usuario)
        if len(solicitudes) > 0:
            solicitudServicioFilter = SolicitudServicioEmpresaFilter(request.GET, queryset=solicitudes)
            solicitudes = solicitudServicioFilter.qs
            if len(solicitudes) > 0:
                solicitudes = solicitudes.order_by('-fecha')
                paginator = Paginator(solicitudes, 10)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request, 'solicitudServicioEmpresa.html', {'page_obj': page_obj,
                                                                         'num_solicitudes': solicitudes.count(),
                                                                         'solicitudServicioFilter': solicitudServicioFilter})
            else:
                msg_error = "No existe ninguna solicitud de servicio con los filtros introducidos."
                return render(request, 'solicitudServicioEmpresa.html', {'msg_error': msg_error})
        else:
            return render(request, 'solicitudServicioEmpresa.html')
    else:
        return redirect('/errorPermiso/')


@login_required
def create_solicitud_servicio_empresa(request):
    if esEmpresa(request):
        if request.method == 'POST':
            form = CreateSolicitudServicioEmpresaForm(
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
                return redirect("/empresa/solicitudServicio/")
        else:
            form = CreateSolicitudServicioEmpresaForm()
            return render(request, 'createSolicitudServicioEmpresa.html', {'form': form})
    else:
        return redirect('/errorPermiso/')


@login_required
def show_solicitud_servicio_empresa(request, id):
    if esEmpresa(request):
        solicitud = SolicitudServicio.objects.get(id=id)
        if request.user == solicitud.usuario:
            return render(request, 'solicitudServicioEmpresaForm.html', {'solicitud': solicitud})
        else:
            return redirect('/errorPermiso')
    else:
        return redirect('/errorPermiso/')


@login_required
def edit_solicitud_servicio_empresa(request, id):
    if esEmpresa(request):
        solicitud = SolicitudServicio.objects.get(id=id)
        if request.user == solicitud.usuario:
            if request.method == 'POST':
                if solicitud.estado == 'Atendida':
                    form = EditSolicitudServicioEmpresaForm(
                        request.POST, request.FILES)
                    if form.is_valid():
                        estado = form.cleaned_data['estado']
                        solicitud.estado = estado
                        solicitud.save()
                        if estado == 'Rechazada':
                            return redirect("/empresa/solicitudServicio/show/" + str(solicitud.id))
                        elif estado == 'Aceptada':
                            servicio = Servicio(
                                solicitudServicio=solicitud, estado="Pendiente")
                            servicio.save()
                            return redirect("/empresa/servicio/show/" + str(servicio.id))
                else:
                    msg_error = "Exclusivamente se puede editar una solicitud de servicio si su estado es 'Atendida'"
                    return render(request, 'solicitudServicioEmpresaForm.html', {'solicitud': solicitud,
                                                                                 'msg_error': msg_error})
            else:
                form = EditSolicitudServicioEmpresaForm()
                return render(request, 'solicitudServicioEmpresaForm.html', {'solicitud': solicitud, 'form': form})
        else:
            return redirect('/errorPermiso')
    else:
        return redirect('/errorPermiso/')
 