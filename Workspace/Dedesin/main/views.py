import string

from django.contrib.auth import authenticate, login
from django.contrib.auth import login as do_login
from django.shortcuts import render, get_object_or_404, redirect
from .models import *

# Create your views here.
from .forms import *


def index(request):
    return render(request, 'home.html')


def tratamientos(request):
    return render(request, 'tratamientos.html')


def errorPermiso(request):
    return render(request, 'errorPermiso.html')

def handler404(request, exception):
    return render(request, '404.html', status=404)

def inicioSesion(request):
    if request.method == "POST":
        form = InicioSesionForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            contraseña = form.cleaned_data['contraseña']
            usuario = authenticate(username=email, password=contraseña)
            if usuario is not None:
                try:
                    empresa = Empresa.objects.filter(usuario=usuario)[0]
                    do_login(request, usuario)
                    return redirect('/empresa/')
                except:
                    persona = Persona.objects.filter(usuario=usuario)[0]
                    try:
                        cliente = Cliente.objects.filter(persona=persona)[0]
                        do_login(request, usuario)
                        return redirect('/cliente/')
                    except:
                        try:
                            trabajador = Trabajador.objects.filter(persona=persona)[0]
                            do_login(request, usuario)
                            return redirect('/trabajador/')
                        except:
                            administrador = Administrador.objects.filter(persona=persona)[0]
                            do_login(request, usuario)
                            return redirect('/administrador/')
            else:
                er_msg = "Error al introducir los datos. No coincide ningún usuario con los datos introducidos."
                return render(request, "auth/inicioSesion.html", {form: 'form', 'er_msg': er_msg})

    form = InicioSesionForm()
    return render(request, "auth/inicioSesion.html", {'form': form})


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
            usuario = User(username=email)
            usuario.set_password(contraseña)
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
                # usuario = authenticate(username=email, password=contraseña)
                login(request, usuario)
                return redirect('/cliente/')
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
                    # usuario = authenticate(username=email, password=contraseña)
                    login(request, usuario)
                    return redirect('/cliente/')
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
            usuario = User(username=email)
            usuario.set_password(contraseña)
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
                    login(request, usuario)
                    return redirect('/empresa/')
                except:
                    usuario.delete()
                    return render(request, 'auth/registroEmpresa.html',
                                  {'form': form, 'er_msg': 'Ya existe una empresa con el CIF introducido.'})

        else:
            return render(request, 'auth/registroEmpresa.html', {'form': form, 'form.errors': form.errors})

    form = RegistroEmpresaForm()
    return render(request, 'auth/registroEmpresa.html', {'form': form})
