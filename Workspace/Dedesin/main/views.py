import string

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
                usuario = Usuario.objects.get(email=email)
                if usuario.contraseña == contraseña:
                    try:
                        empresa = Empresa.objects.get(usuario=usuario)
                        return render(request, 'inicioSesionCliente.html',
                                      {'form': form, 'ex_msg': 'Ha iniciado correctamente sesión.'})
                    except:
                        persona = Persona.objects.get(usuario=usuario)
                        cliente = Cliente.objects.get(persona=persona)
                        if cliente:
                            return render(request, 'inicioSesionCliente.html',
                                          {'form': form, 'ex_msg': 'Ha iniciado correctamente sesión.'})
                else:
                    return render(request, 'inicioSesionCliente.html ',
                                  {'form': form, 'er_msg': 'Contraseña incorrecto.'})
            except:
                return render(request, 'inicioSesionCliente.html ',
                              {'form': form, 'er_msg': 'No existe ningún usuario con el email introducido.'})

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
            if cuenta_bancaria == '':
                cuenta_bancaria = None
                print(cuenta_bancaria)
            email = form.cleaned_data['email']
            contraseña = form.cleaned_data['contraseña']
            usuario = Usuario(email=email, contraseña=contraseña)
            try:
                usuario.save()
            except:
                return render(request, 'registroCliente.html',
                              {'er_msg': 'El usuario ya existe en la base de datos', 'form': form})

            persona = Persona(nombre=nombre, apellidos=apellidos, dni=dni, telefono=telefono, usuario=usuario)
            try:
                persona.save()
            except:
                usuario.delete()
                return render(request, 'registroCliente.html',
                              {'er_msg': 'Ya existe un usuario con el DNI/Telefono introducidos', 'form': form})

            cliente = Cliente(direccion=direccion, cuenta_bancaria=cuenta_bancaria, persona=persona)
            if not cuenta_bancaria:
                cliente.save()
            else:
                cuentas_bancarias_clientes = []
                cuentas_bancarias_empresas = []
                for c in Cliente.objects.all():
                    cuentas_bancarias_clientes.append(c.cuenta_bancaria)
                for e in Empresa.objects.all():
                    cuentas_bancarias_empresas.append(e.cuenta_bancaria)

                if (cuenta_bancaria in cuentas_bancarias_empresas) or (cuenta_bancaria in cuentas_bancarias_clientes):
                    persona.delete()
                    usuario.delete()
                    return render(request, 'registroCliente.html',
                                  {'er_msg': 'La cuenta bancaria introducida ya existe', 'form': form})
                else:
                    cliente.save()
            return render(request, 'home.html', {'ex_msg': 'El registro se ha realizado correctamente.', 'form': form})
        else:
            return render(request, 'registroCliente.html', {'form': form, 'form.errors': form.errors})

    form = RegistroClienteForm()
    return render(request, 'registroCliente.html', {'form': form})
