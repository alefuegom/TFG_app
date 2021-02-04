import string

from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.
from .forms import *


def index(request):
    return render(request, 'home.html')

def tratamientos(request):
    return render(request, 'tratamientos.html')


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
                        return render(request, 'auth/inicioSesion.html',
                                      {'form': form, 'ex_msg': 'Ha iniciado correctamente sesión.'})
                    except:
                        persona = Persona.objects.get(usuario=usuario)
                        cliente = Cliente.objects.get(persona=persona)
                        return render(request, '/cliente/inicioCliente',
                                          {'form': form, 'cliente':cliente})
                else:
                    return render(request, 'auth/inicioSesion.html ',
                                  {'form': form, 'er_msg': 'Contraseña incorrecto.'})
            except:
                return render(request, 'auth/inicioSesion.html ',
                              {'form': form, 'er_msg': 'No existe ningún usuario con el email introducido.'})

    form = InicioSesionForm()
    return render(request, 'auth/inicioSesion.html', {'form': form})


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
            email = form.cleaned_data['email']
            contraseña = form.cleaned_data['contraseña']
            usuario = Usuario(email=email, contraseña=contraseña)
            try:
                usuario.save()
            except:
                return render(request, 'auth/registroCliente.html',
                              {'er_msg': 'Ya existe un usuario con el email introducido.', 'form': form})

            persona = Persona(nombre=nombre, apellidos=apellidos, dni=dni, telefono=telefono, usuario=usuario)
            telefonos = []
            for p in Persona.objects.all():
                telefonos.append(p.telefono)
            for e in Empresa.objects.all():
                telefonos.append(e.telefono)
            if telefono in telefonos:
                usuario.delete()
                return render(request, 'auth/registroCliente.html',
                              {'er_msg': 'Ya existe un usuario con el número de teléfono introducido', 'form': form})
            try:
                persona.save()
            except:
                usuario.delete()
                return render(request, 'auth/registroCliente.html',
                          {'er_msg': 'Ya existe un usuario con el DNI introducido', 'form': form})

            cliente = Cliente(direccion=direccion, cuenta_bancaria=cuenta_bancaria, persona=persona)
            if not cuenta_bancaria:
                cliente.save()
            else:
                cuentas_bancarias = []
                for c in Cliente.objects.all():
                    cuentas_bancarias.append(c.cuenta_bancaria)
                for e in Empresa.objects.all():
                    cuentas_bancarias.append(e.cuenta_bancaria)
                if cuenta_bancaria in cuentas_bancarias:
                    persona.delete()
                    usuario.delete()
                    return render(request, 'auth/registroCliente.html',
                                  {'er_msg': 'Ya existe un usuario con la cuenta bancaria introducida.', 'form': form})
                else:
                    cliente.save()
                    return render(request, 'home.html', {'ex_msg': 'El registro se ha realizado correctamente.', 'form': form})
        else:
            return render(request, 'auth/registroCliente.html', {'form': form, 'form.errors': form.errors})
    form = RegistroClienteForm()
    return render(request, 'auth/registroCliente.html', {'form': form})


def registroEmpresa(request):
    if request.method == 'POST':
        form = RegistroEmpresaForm(request.POST, request.FILES)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            cif = form.cleaned_data['CIF']
            direccion = form.cleaned_data['direccion']
            telefono = form.cleaned_data['telefono']
            cuenta_bancaria = form.cleaned_data['cuenta_bancaria']
            email = form.cleaned_data['email']
            contraseña = form.cleaned_data['contraseña']
            usuario = Usuario(email=email, contraseña=contraseña)
            try:
                usuario.save()
            except:
                return render(request, 'auth/registroEmpresa.html',
                              {'form': form, 'er_msg': 'Ya existe un usuario con el email introducido..'})

            empresa = Empresa(nombre=nombre, cif=cif, direccion=direccion, telefono=telefono,
                              cuenta_bancaria=cuenta_bancaria, usuario=usuario)
            cuentas_bancarias = []
            telefonos = []
            for c in Cliente.objects.all():
                cuentas_bancarias.append(c.cuenta_bancaria)
                telefonos.append(c.persona.telefono)
            for e in Empresa.objects.all():
                cuentas_bancarias.append(e.cuenta_bancaria)
                telefonos.append(e.telefono)
            if cuenta_bancaria in cuentas_bancarias:
                usuario.delete()
                return render(request, 'auth/registroEmpresa.html',
                              {'form': form, 'er_msg': 'Ya existe un usuario con la cuenta bancaria introducida.'})
            if telefono in telefonos:
                usuario.delete()
                return render(request, 'auth/registroEmpresa.html',
                              {'form': form, 'er_msg': 'Ya existe un usuario con el número de telefono introducido.'})
            else:
                try:
                    empresa.save()
                    return render(request, 'auth/registroEmpresa.html',
                                  {'ex_msg': 'El registro se ha realizado correctamente.', 'form': form})
                except:
                    usuario.delete()
                    return render(request, 'auth/registroEmpresa.html',
                                  {'form': form, 'er_msg': 'Ya existe una empresa con el CIF introducido.'})

        else:
            return render(request, 'auth/registroEmpresa.html', {'form': form, 'form.errors': form.errors})

    form = RegistroEmpresaForm()
    return render(request, 'auth/registroEmpresa.html', {'form': form})
