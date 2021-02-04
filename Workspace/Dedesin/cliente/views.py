from django.shortcuts import render

# Create your views here.


def inicio_cliente(request):
    return render(request, 'inicioCliente.html')


def solicitud_servicio_cliente(request):
    #solicitudes = SolicitudServicio.objects.filter(usuario='cliente1@cliente.com')
    # return render(request, 'solicitudServicioCliente.html', {'solicitudes': solicitudes})
    return render(request, 'solicitudServicioCliente.html')


def servicio_cliente(request):
    return render(request, 'servicioCliente.html')


def perfil_cliente(request):
    return render(request, 'perfilCliente.html')

def solicitud_servicio_cliente_form(request):
    return render(request, 'solicitudServicioClienteForm.html')

def solicitud_servicio_cliente_form(request):
    return render(request, 'servicioClienteForm.html')