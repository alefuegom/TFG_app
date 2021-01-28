from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.
from .forms import *


def index(request):
    return render(request, 'home.html')


def inicioSesion(request):
    if request.method == 'GET':
        form = InicioSesionForm(request.GET, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            contraseña = form.cleaned_data['contraseña']
            try:
                usuario = get_object_or_404(Usuario, email=email)
                if usuario:
                    persona = Persona.objects.get(usuario=usuario)
                    if persona:
                        cliente = Cliente.objects.get(persona=persona)
                        print("CLIENTASO")
                        return render(request, 'home.html', {'ex_msg': 'Se ha logueado perfectamente como cliente'})
                    else:
                        empresa = Empresa.objects.get(usuario=usuario)
                        return render(request, 'home.html', {'ex_msg': 'Se ha logueado perfectamente como empresa'})
            except:
                return (request, 'inicioSesion.html', {'form': form,
                                                       'er_msg': 'No se ha encontrado ninguna cuenta asociada o su contraseña es incorrecta'})
    form = InicioSesionForm()
    return render(request, 'inicioSesionCliente.html', {'form': form})


def registroCliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST, request.FILES)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellidos = form.cleaned_data['apellidos']
            dni = form.cleaned_data['dni']
            direccion = form.cleaned_data['direccion']
            telefono = form.cleaned_data['telefono']
            cuenta_bancaria = form.cleaned_data['cuenta_bancaria']
            email = form.cleaned_data['email']
            contraseña = form.cleaned_data['contraseña']
            print("FUNCIONA")
            usuario = Usuario(email=email, contraseña=contraseña)
            usuario.save()
            persona = Persona(nombre=nombre, apellidos=apellidos, dni=dni, telefono=telefono, usuario=usuario)
            persona.save()
            cliente = Cliente(direccion=direccion,
                              cuenta_bancaria=cuenta_bancaria, persona=persona)
            cliente.save()
            return render(request, 'home.html', {'ex_msg': 'El registro se ha realizado correctamente.'})
    form = RegistroClienteForm()
    return render(request, 'registroCliente.html', {'form': form})
