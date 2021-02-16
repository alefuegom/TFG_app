from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from .forms import *
from ..models import *
from django.contrib.auth import logout as do_logout


# VISTAS GENERALES
@login_required
def inicio_empresa(request):
    return render(request, 'inicioEmpresa.html')


@login_required
def show_perfil_empresa(request):
    empresa = Empresa.objects.filter(usuario=request.user)[0]
    return render(request, 'perfilEmpresa.html', {'empresa': empresa})


@login_required
def edit_perfil_empresa(request):
    empresa = Empresa.objects.filter(usuario=request.user)[0]
    if request.method == 'POST':
        form = EditPerfilEmpresaForm(request.POST, request.FILES)
        if form.is_valid():
            print("ES VALIDO BRO")
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


# CRUD SERVICIOS
@login_required
def list_servicios_empresa(request):
    usuario = User.objects.filter(username=request.user.username)[0]
    solicitudes = SolicitudServicio.objects.filter(usuario=usuario)
    servicios = []
    for solicitud in solicitudes:
        servicio = Servicio.objects.filter(solicitudServicio=solicitud)
        if servicio:
            servicios.append(servicio[0])
    if servicios:
        return render(request, 'servicioEmpresa.html', {'servicios': servicios, 'num_servicios': len(servicios)})
    else:
        return render(request, 'servicioEmpresa.html')


@login_required
def show_servicios_empresa(request, id):
    servicio = Servicio.objects.get(id=id)
    if servicio:
        if request.user == servicio.solicitudServicio.usuario:
            return render(request, 'servicioEmpresaForm.html', {'servicio': servicio})
        else:
            return redirect('/errorPermiso')
    else:
        return render(request, 'servicioEmpresaForm.html')


# CRUD SOLICITUD DE SERVICIO
@login_required
def list_solicitud_servicio_empresa(request):
    usuario = User.objects.filter(username=request.user.username)[0]
    solicitudes = SolicitudServicio.objects.filter(usuario=usuario)
    if solicitudes:
        return render(request, 'solicitudServicioEmpresa.html', {'solicitudes': solicitudes,
                                                                 'num_solicitudes': solicitudes.count()})
    else:
        return render(request, 'solicitudServicioEmpresa.html')


@login_required
def create_solicitud_servicio_empresa(request):
    if request.method == 'POST':
        form = CreateSolicitudServicioEmpresaForm(request.POST, request.FILES)
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


@login_required
def show_solicitud_servicio_empresa(request, id):
    solicitud = SolicitudServicio.objects.get(id=id)
    if request.user == solicitud.usuario:
        return render(request, 'solicitudServicioEmpresaForm.html', {'solicitud': solicitud})
    else:
        return redirect('/errorPermiso')


@login_required
def edit_solicitud_servicio_empresa(request, id):
    solicitud = SolicitudServicio.objects.get(id=id)
    if request.user == solicitud.usuario:
        if request.method == 'POST':
            form = EditSolicitudServicioEmpresaForm(request.POST, request.FILES)
            if form.is_valid():
                estado = form.cleaned_data['estado']
                solicitud.estado = estado
                solicitud.save()
                return redirect("/empresa/solicitudServicio/show/" + str(solicitud.id))
        else:
            form = EditSolicitudServicioEmpresaForm()
            return render(request, 'solicitudServicioEmpresaForm.html', {'solicitud': solicitud, 'form': form})
    else:
        return redirect('/errorPermiso')


def logout(request):
    do_logout(request)
    return redirect('/')
