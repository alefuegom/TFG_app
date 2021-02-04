from django.shortcuts import render

# Create your views here.


def inicio_empresa(request):
    return render(request, 'inicioEmpresa.html')


def solicitud_servicio_empresa(request):
    #solicitudes = SolicitudServicio.objects.filter(usuario='empresa1@cliente.com')
    # return render(request, 'solicitudServicioCliente.html', {'solicitudes': solicitudes})
    return render(request, 'solicitudServicioEmpresa.html')


def servicio_empresa(request):
    return render(request, 'servicioEmpresa.html')


def perfil_empresa(request):
    return render(request, 'perfilEmpresa.html')

def solicitud_servicio_empresa_form(request):
    return render(request, 'solicitudServicioEmpresaForm.html')

def solicitud_servicio_empresa_form(request):
    return render(request, 'servicioEmpresaForm.html')