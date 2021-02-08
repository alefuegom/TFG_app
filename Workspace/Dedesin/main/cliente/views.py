from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from .forms import *
from ..models import *
from django.contrib.auth import logout as do_logout


@login_required
def inicio_cliente(request):
    return render(request, 'inicioCliente.html')


def servicio_cliente(request):
    return render(request, 'servicioCliente.html')


def perfil_cliente(request):
    return render(request, 'perfilCliente.html')


@login_required
def list_solicitud_servicio_cliente(request):
    usuario = User.objects.filter(username=request.user.username)[0]
    solicitudes = SolicitudServicio.objects.filter(usuario=usuario)
    if solicitudes:
        return render(request, 'solicitudServicioCliente.html', {'solicitudes': solicitudes,
                                                                 'num_solicitudes': solicitudes.count()})
    else:
        return render(request, 'solicitudServicioCliente.html')


@login_required
def create_solicitud_servicio_cliente(request):
    if request.method == 'POST':
        form = CreateSolicitudServicioClienteForm(request.POST, request.FILES)
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


@login_required
def show_solicitud_servicio_cliente(request, id):
    solicitud = SolicitudServicio.objects.get(id=id)

    return render(request, 'solicitudServicioClienteForm.html', {'solicitud': solicitud})


@login_required
def edit_solicitud_servicio_cliente(request, id):
    solicitud = SolicitudServicio.objects.get(id=id)
    if request.method == 'POST':
        form = EditSolicitudServicioClienteForm(request.POST, request.FILES)
        if form.is_valid():
            estado = form.cleaned_data['estado']
            solicitud.estado = estado
            solicitud.save()
            return redirect("/cliente/solicitudServicio/show/" + str(solicitud.id))
    else:
        form = EditSolicitudServicioClienteForm()
        return render(request, 'solicitudServicioClienteForm.html', {'solicitud': solicitud, 'form': form})


def logout(request):
    do_logout(request)
    return redirect('/')
