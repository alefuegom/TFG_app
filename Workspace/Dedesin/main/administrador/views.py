from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from django.contrib.auth import logout as do_logout

from .forms import *
from ..models import *


# MÉTODOS AUXILIARES
def esAdministrador(request):
    try:
        persona = Persona.objects.filter(usuario=request.user)[0]
        administrador = Administrador.objects.filter(persona=persona)[0]
        return administrador
    except:
        return None


# VISTAS GENERALES
@login_required
def cerrarSesion(request):
    do_logout(request)
    return redirect('/')


@login_required
def inicioAdministrador(request):
    if esAdministrador(request):
        return render(request, 'inicioAdministrador.html')
    else:
        return redirect('/errorPermiso/')


@login_required
def show_perfil_administrador(request):
    if esAdministrador(request):
        persona = Persona.objects.filter(usuario=request.user)[0]
        administrador = Administrador.objects.filter(persona=persona)[0]
        return render(request, 'perfilAdministrador.html', {'administrador': administrador})
    else:
        return redirect('/errorPermiso/')


@login_required
def edit_perfil_administrador(request):
    if esAdministrador(request):
        persona = Persona.objects.filter(usuario=request.user)[0]
        if request.method == 'POST':
            form = EditPerfilAdministrador(request.POST, request.FILES)
            if form.is_valid():
                persona.dni = form.cleaned_data['dni']
                persona.nombre = form.cleaned_data['nombre']
                persona.apellidos = form.cleaned_data['apellidos']
                persona.telefono = form.cleaned_data['telefono']
                persona.usuario.username = form.cleaned_data['email']
                persona.usuario.save()
                persona.save()
                return redirect('/administrador/miPerfil/')
            else:
                valores = [persona.nombre, persona.apellidos,
                           persona.usuario.username, persona.dni, persona.telefono]
                items = zip(form, valores)
                return render(request, 'perfilAdministrador.html', {'form': form, 'items': items})
        else:
            form = EditPerfilAdministrador()
            valores = [persona.nombre, persona.apellidos,
                       persona.usuario.email, persona.dni, persona.telefono]
            items = zip(form, valores)
            return render(request, 'perfilAdministrador.html', {'form': form, 'items': items})
    else:
        return redirect('/errorPermiso/')


# CRUD SOLICITUD SERVICIO
@login_required
def list_solicitudServicio_administrador(request):
    if esAdministrador(request):
        solicitudes = SolicitudServicio.objects.all()
        return render(request, 'solicitudServicioAdministrador.html', {'solicitudes': solicitudes, 'num_solicitudes':
            len(solicitudes)})
    else:
        return redirect('/errorPermiso/')


@login_required
def show_solicitudServicio_administrador(request, id):
    if esAdministrador(request):
        solicitud = SolicitudServicio.objects.get(id=id)
        try:
            empresa = Empresa.objects.filter(usuario=solicitud.usuario)[0]
            return render(request, 'solicitudServicioAdministradorForm.html',
                          {'solicitud': solicitud, 'empresa': empresa})
        except:
            persona = Persona.objects.filter(usuario=solicitud.usuario)[0]
            cliente = Cliente.objects.filter(persona=persona)[0]
            return render(request, 'solicitudServicioAdministradorForm.html',
                          {'solicitud': solicitud, 'cliente': cliente})
    else:
        return redirect('/errorPermiso/')


@login_required
def edit_solicitudServicio_administrador(request, id):
    if esAdministrador(request):
        solicitud = SolicitudServicio.objects.get(id=id)
        if solicitud.estado == 'Pendiente':
            if request.method == 'POST':
                form = EditSolicitudServicioAdministradorForm(
                    request.POST, request.FILES)
                if form.is_valid():
                    try:
                        fecha_str = form.cleaned_data['fecha']
                        solicitud.fecha = datetime.strptime(
                            fecha_str, "%d/%m/%Y").date()
                        if solicitud.fecha <= date.today():
                            msg_error = "La fecha debe ser posterior a la fecha actual."
                            return render(request, 'solicitudServicioAdministradorForm.html',
                                          {'form': form, 'solicitud_edit': solicitud,
                                           'msg_error': msg_error})
                        solicitud.tratamiento = Tratamiento.objects.get(
                            id=form.cleaned_data['tratamiento'])
                        if solicitud.tratamiento.plaga != solicitud.plaga:
                            msg_error = "La plaga que combate el tratamiento debe ser igual a la plaga introducida en la solicitud de servicio."
                            return render(request, 'solicitudServicioAdministradorForm.html',
                                          {'form': form, 'solicitud_edit': solicitud,
                                           'msg_error': msg_error})
                        solicitud.estado = 'Atendida'
                        solicitud.save()
                        return redirect('/administrador/solicitudServicio/')
                    except:
                        msg_error = "Introduzca un formato de fecha correcto (dd/mm/yyyy)"
                        return render(request, 'solicitudServicioAdministradorForm.html',
                                      {'form': form, 'solicitud_edit': solicitud,
                                       'msg_error': msg_error})
                else:
                    return render(request, 'solicitudServicioAdministradorForm.html',
                                  {'solicitud_edit': solicitud, 'form': form})
            else:
                form = EditSolicitudServicioAdministradorForm()
                return render(request, 'solicitudServicioAdministradorForm.html',
                              {'solicitud_edit': solicitud, 'form': form})
        else:
            msg_error = 'Exclusivamente se puede editar una solicitud de servicio ' \
                        'si su estado tiene el valor de "Pendiente".'
            return render(request, 'solicitudServicioAdministradorForm.html',
                          {'solicitud': solicitud, 'msg_error': msg_error})
    else:
        return redirect('/errorPermiso/')


# CRUD SERVICIOS
@login_required
def list_servicio_administrador(request):
    if esAdministrador(request):
        servicios = Servicio.objects.all()
        return render(request, 'servicioAdministrador.html', {'servicios': servicios, 'num_servicios': len(servicios)})
    else:
        return redirect('/errorPermiso/')


@login_required
def show_servicio_administrador(request, id):
    if esAdministrador(request):
        servicio = Servicio.objects.get(id=id)
        try:
            empresa = Empresa.objects.filter(
                usuario=servicio.solicitudServicio.usuario)[0]
            return render(request, 'servicioAdministradorForm.html', {'servicio': servicio, 'empresa': empresa})
        except:
            persona = Persona.objects.filter(
                usuario=servicio.solicitudServicio.usuario)[0]
            cliente = Cliente.objects.filter(persona=persona)[0]
            return render(request, 'servicioAdministradorForm.html', {'servicio': servicio, 'cliente': cliente})
    else:
        return redirect('/errorPermiso/')


@login_required
def edit_servicio_administrador(request, id):
    if esAdministrador(request):
        servicio = Servicio.objects.get(id=id)
        if servicio.estado == "Pendiente":
            if request.method == 'POST':
                form = EditServicioAdministradorForm(
                    request.POST, request.FILES)
                if form.is_valid():
                    servicio.trabajador = Trabajador.objects.get(
                        id=form.cleaned_data['trabajador'])
                    servicio.save()
                    return redirect('/administrador/servicio/')
            else:
                form = EditServicioAdministradorForm()
                return render(request, 'servicioAdministradorForm.html', {'servicio_edit': servicio,
                                                                          'form': form})
        else:
            msg_error = 'Exclusivamente se puede editar un servicio ' \
                        'si su estado tiene el valor de "Pendiente".'
            return render(request, 'servicioAdministradorForm.html', {'servicio': servicio, 'msg_error': msg_error})
    else:
        return redirect('/errorPermiso/')


# CRUD PLAGAS
@login_required()
def list_plaga_administrador(request):
    if esAdministrador(request):
        plagas = Plaga.objects.all()
        if len(plagas) > 0:
            return render(request, 'plagaAdministrador.html', {'plagas': plagas, 'num_plagas': len(plagas)})
        else:
            return render(request, 'plagaAdministrador.html')

    else:
        return redirect('/errorPermiso/')


@login_required()
def create_plaga_administrador(request):
    if esAdministrador(request):
        if request.method == 'POST':
            form = CreatePlagaAdministradorForm(request.POST, request.FILES)
            if form.is_valid():
                nombre = form.cleaned_data['nombre']
                if len(Plaga.objects.filter(nombre=nombre)) == 0:
                    plaga = Plaga(nombre=nombre)
                    plaga.save()
                    return redirect('/administrador/plaga')
                else:
                    msg_error = "Ya existe una plaga con el nombre introducido."
                    return render(request, 'plagaAdministradorForm.html', {'form': form, 'msg_error': msg_error})
            else:
                return render(request, 'plagaAdministradorForm.html', {'form': form})
        else:
            form = CreatePlagaAdministradorForm()
            return render(request, 'plagaAdministradorForm.html', {'form': form})
    else:
        return redirect('/errorPermiso/')


@login_required()
def delete_plaga_administrador(request, id):
    if esAdministrador(request):
        plaga = Plaga.objects.get(id=id)
        solicitudesServicio = SolicitudServicio.objects.filter(plaga=plaga)
        msg_error = ""
        if len(solicitudesServicio) > 0:
            msg_error = "No se puede eliminar una plaga que está presente en una solicitud de servicio."
        tratamientos = Tratamiento.objects.filter(plaga=plaga)
        if len(tratamientos) > 0:
            msg_error = "No se puede eliminar una plaga que está presente en un tratamiento."
        if msg_error:
            plagas = Plaga.objects.all()
            return render(request, 'plagaAdministrador.html', {'plagas': plagas, 'num_plagas': len(plagas),
                                                               'msg_error': msg_error})
        plaga.delete()
        return redirect('/administrador/plaga')
    else:
        return redirect('/errorPermiso/')


# CRUD TRATAMIENTOS

@login_required()
def list_tratamiento_administrador(request):
    if esAdministrador(request):
        tratamientos = Tratamiento.objects.all()
        if len(tratamientos) > 0:
            return render(request, 'tratamientoAdministrador.html',
                          {'tratamientos': tratamientos, 'num_tratamientos': len(tratamientos)})
        else:
            return render(request, 'tratamientoAdministrador.html')
    else:
        return redirect('/errorPermiso/')


@login_required()
def show_tratamiento_administrador(request, id):
    if esAdministrador(request):
        tratamiento = Tratamiento.objects.get(id=id)
        return render(request, 'tratamientoAdministradorForm.html', {'tratamiento': tratamiento})
    else:
        return redirect('/errorPermiso/')


@login_required()
def create_tratamiento_administrador(request):
    if esAdministrador(request):
        if request.method == 'POST':
            form = CreateTratamientoAdministradorForm(request.POST, request)
            if form.is_valid():
                nombre = form.cleaned_data['nombre']
                descripcion = form.cleaned_data['descripcion']
                precio = form.cleaned_data['precio']
                abandono = form.cleaned_data['abandono']
                horasAbandono = form.cleaned_data['horasAbandono']
                plaga = Plaga.objects.get(id=form.cleaned_data['plaga'])
                if not abandono and horasAbandono != 0:
                    msg_error = "No se puede rellenar el tiempo de abandono, si el tratamiento no requiere abandono."
                    return render(request, 'tratamientoAdministradorForm.html',
                                  {'form': form, 'msg_error': msg_error})
                if abandono and horasAbandono <= 0:
                    msg_error = "Si el tratamiento necesita que se abanone la zona tratada, el valor del tiempo no puede ser 0."
                    return render(request, 'tratamientoAdministradorForm.html',
                                  {'form': form, 'msg_error': msg_error})
                else:
                    tratamiento = Tratamiento(nombre=nombre, descripcion=descripcion, precio=precio, abandono=abandono,
                                              horasAbandono=horasAbandono, plaga=plaga)
                    tratamiento.save()
                    return redirect('/administrador/tratamiento/')
            else:
                return render(request, 'tratamientoAdministradorForm.html', {'form': form})
        else:
            form = CreateTratamientoAdministradorForm()
            return render(request, 'tratamientoAdministradorForm.html', {'form': form})
    else:
        return redirect('/errorPermiso/')


@login_required()
def edit_tratamiento_administrador(request, id):
    if esAdministrador(request):
        tratamiento = Tratamiento.objects.get(id=id)
        if request.method == 'POST':
            form = EditTratamientoAdministradorForm(
                request.POST, request.FILES)
            if form.is_valid():
                abandono = form.cleaned_data['abandono']
                horasAbandono = form.cleaned_data['horasAbandono']
                if not abandono and horasAbandono != 0:
                    msg_error = "No se puede rellenar el tiempo de abandono, si el tratamiento no requiere abandono."
                    valores = [tratamiento.nombre, tratamiento.plaga, tratamiento.precio,
                               tratamiento.abandono, tratamiento.horasAbandono, tratamiento.descripcion]
                    items = zip(form, valores)
                    return render(request, 'tratamientoAdministradorForm.html', {'items': items,
                                                                                 'form': form, 'msg_error': msg_error})

                if abandono and horasAbandono <= 0:
                    msg_error = "Si el tratamiento necesita que se abanone la zona tratada, el valor del tiempo no puede ser 0."
                    valores = [tratamiento.nombre, tratamiento.plaga, tratamiento.precio,
                               tratamiento.abandono, tratamiento.horasAbandono, tratamiento.descripcion]
                    items = zip(form, valores)
                    return render(request, 'tratamientoAdministradorForm.html', {'items': items,
                                                                                 'form': form, 'msg_error': msg_error})
                else:
                    tratamiento.nombre = form.cleaned_data['nombre']
                    tratamiento.descripcion = form.cleaned_data['descripcion']
                    tratamiento.plaga = Plaga.objects.get(
                        id=form.cleaned_data['plaga'])
                    tratamiento.abandono = abandono
                    tratamiento.horasAbandono = horasAbandono
                    tratamiento.save()
                    return redirect("/administrador/tratamiento/show/" + str(tratamiento.id) + "/")
            else:
                print(form.errors)
                valores = [tratamiento.nombre, tratamiento.plaga, tratamiento.precio,
                           tratamiento.abandono, tratamiento.horasAbandono, tratamiento.descripcion]
                items = zip(form, valores)
                return render(request, 'tratamientoAdministradorForm.html', {'form_edit': form, 'items': items,
                                                                             'tratamiento_edit': tratamiento})
        else:
            form = EditTratamientoAdministradorForm()
            valores = [tratamiento.nombre, tratamiento.plaga, tratamiento.precio,
                       tratamiento.abandono, tratamiento.horasAbandono, tratamiento.descripcion]
            items = zip(form, valores)
            return render(request, 'tratamientoAdministradorForm.html', {'form_edit': form, 'items': items,
                                                                         'tratamiento_edit': tratamiento, })
    else:
        return redirect('/errorPermiso/')


@login_required()
def delete_tratamiento_administrador(request, id):
    if esAdministrador(request):
        tratamiento = Tratamiento.objects.get(id=id)
        solicitudes = SolicitudServicio.objects.filter(tratamiento=tratamiento)
        if len(solicitudes) != 0:
            tratamientos = Tratamiento.objects.all()
            msg_error = "No se puede eliminar un tratamiento que esta presente en una solicitud de servicio."
            return render(request, 'tratamientoAdministrador.html',
                          {'tratamientos': tratamientos, 'num_tratamientos': len(tratamientos),
                           'msg_error': msg_error})
        else:
            tratamiento.delete()
            return redirect('/administrador/tratamiento/')

    else:
        return redirect('/errorPermiso/')


# FACTURAS
@login_required()
def list_facturas_administrador(request):
    if esAdministrador(request):
        servicios = Servicio.objects.exclude(factura=None)
        return render(request, 'facturaAdministrador.html', {'servicios': servicios, 'num_servicios': len(servicios)})
    else:
        return redirect('/errorPermiso/')


@login_required()
def show_factura_administrador(request, id):
    if esAdministrador(request):
        servicio = Servicio.objects.get(id=id)
        factura = servicio.factura
        return render(request, 'facturaAdministradorForm.html', {'servicio': servicio, 'factura': factura})
    else:
        return redirect("/errorPermiso/")


# CRUD VEHICULOS
@login_required()
def list_vehiculo_administrador(request):
    if esAdministrador(request):
        vehiculos = Vehiculo.objects.all()
        if len(vehiculos) > 0:
            return render(request, 'vehiculoAdministrador.html',
                          {'vehiculos': vehiculos, 'num_vehiculos': len(vehiculos)})
        else:
            return render(request, 'vehiculoAdministrador.html')
    else:
        return redirect('/errorPermiso/')


@login_required()
def show_vehiculo_administrador(request, id):
    if esAdministrador(request):
        vehiculo = Vehiculo.objects.get(id=id)
        try:
            trabajador = Trabajador.objects.filter(vehiculo=vehiculo)[0]
            return render(request, 'vehiculoAdministradorForm.html', {'vehiculo': vehiculo, 'trabajador': trabajador})
        except:
            return render(request, 'vehiculoAdministradorForm.html', {'vehiculo': vehiculo})

    else:
        return redirect('/errorPermiso/')


@login_required()
def create_vehiculo_administrador(request):
    if esAdministrador(request):
        if request.method == 'POST':
            form = CreateVehiculoAdministradorForm(request.POST, request.FILES)
            if form.is_valid():
                marca = form.cleaned_data['marca']
                modelo = form.cleaned_data['modelo']
                matricula = form.cleaned_data['matricula']
                fecha_matriculacion = form.cleaned_data['fecha_matriculacion']
                proxima_revision = form.cleaned_data['proxima_revision']
                try:
                    fecha_matriculacion = datetime.strptime(
                        fecha_matriculacion, "%d/%m/%Y").date()
                    if fecha_matriculacion > date.today():
                        msg_error = "La fecha de matriculación debe ser anterior a la fecha actual."
                        return render(request, 'vehiculoAdministradorForm.html',
                                      {'form': form,
                                       'msg_error': msg_error})
                except:
                    msg_error = "Introduzca un formato de fecha correcto (dd/mm/yyyy) en el campo de fecha de matriculación "
                    return render(request, 'vehiculoAdministradorForm.html',
                                  {'form': form,
                                   'msg_error': msg_error})
                try:
                    proxima_revision = datetime.strptime(
                        proxima_revision, "%d/%m/%Y").date()
                    if proxima_revision <= date.today():
                        msg_error = "La fecha de la próxima revisión debe ser posterior a la fecha actual."
                        return render(request, 'vehiculoAdministradorForm.html',
                                      {'form': form,
                                       'msg_error': msg_error})
                except:
                    msg_error = "Introduzca un formato de fecha correcto (dd/mm/yyyy) en el campo de fecha de próxima revisión "
                    return render(request, 'vehiculoAdministradorForm.html',
                                  {'form': form,
                                   'msg_error': msg_error})
                vehiculo = Vehiculo(marca=marca, modelo=modelo, matricula=matricula,
                                    fecha_matriculacion=fecha_matriculacion,
                                    proxima_revision=proxima_revision)
                vehiculo.save()
                return redirect('/administrador/vehiculo')
            else:
                return render(request, 'vehiculoAdministradorForm.html', {'form': form})
        else:
            form = CreateVehiculoAdministradorForm()
            return render(request, 'vehiculoAdministradorForm.html', {'form': form})
    else:
        return redirect('/errorPermiso/')


@login_required()
def edit_vehiculo_administrador(request, id):
    if esAdministrador(request):
        vehiculo = Vehiculo.objects.get(id=id)
        if request.method == 'POST':
            form = EditVehiculoAdministradorForm(request.POST, request.FILES)
            if form.is_valid():
                proxima_revision = form.cleaned_data['proxima_revision']
                try:
                    proxima_revision = datetime.strptime(
                        proxima_revision, "%d/%m/%Y").date()
                    if proxima_revision <= date.today():
                        msg_error = "La fecha de la próxima revisión debe ser posterior a la fecha actual."
                        return render(request, 'vehiculoAdministradorForm.html',
                                      {'form_edit': form, 'vehiculo_edit': vehiculo,
                                       'msg_error': msg_error})
                except:
                    msg_error = "Introduzca un formato de fecha correcto (dd/mm/yyyy) en el campo de  fecha de próxima revisión "
                    return render(request, 'vehiculoAdministradorForm.html',
                                  {'form_edit': form, 'vehiculo_edit': vehiculo,
                                   'msg_error': msg_error})
                vehiculo.save()
                return redirect('/administrador/vehiculo')
            else:
                return render(request, 'vehiculoAdministradorForm.html', {'form_edit': form, 'vehiculo_edit': vehiculo})
        else:
            form = EditVehiculoAdministradorForm()
            return render(request, 'vehiculoAdministradorForm.html', {'form_edit': form, 'vehiculo_edit': vehiculo})
    else:
        return redirect('/errorPermiso/')


@login_required()
def delete_vehiculo_administrador(request, id):
    if esAdministrador(request):
        vehiculo = Vehiculo.objects.get(id=id)
        try:
            trabajador = Trabajador.objects.filter(vehiculo=vehiculo)[0]
            vehiculos = Vehiculo.objects.all()
            msg_error = "No se puede dar de baja a un vehículo si está asociado a un trabajador."
            return render(request, 'vehiculoAdministrador.html', {'msg_error': msg_error, 'vehiculos': vehiculos,
                                                                  'num_vehiculos': len(vehiculos)})
        except:
            vehiculo.delete()
            return redirect('/administrador/vehiculo/')
    else:
        return redirect('/errorPermiso/')


# CRUD TRABAJADORES
@login_required()
def list_trabajador_administrador(request):
    if esAdministrador(request):
        trabajadores = Trabajador.objects.all()
        if len(trabajadores) >= 0:
            return render(request, 'trabajadorAdministrador.html', {'trabajadores': trabajadores,
                                                                    'num_trabajadores': len(trabajadores)})
        else:
            return render(request, 'trabajadorAdministrador.html')
    else:
        return redirect('/errorPermiso/')


@login_required()
def show_trabajador_administrador(request, id):
    if esAdministrador(request):
        trabajador = Trabajador.objects.get(id=id)
        trabajador_delete = False
        if len(Servicio.objects.filter(trabajador=trabajador)) == 0:
            trabajador_delete = True
        return render(request, 'trabajadorAdministradorForm.html', {'trabajador': trabajador,
                                                                    'trabajador_delete':trabajador_delete})
    else:
        return redirect('/errorPermiso/')


@login_required()
def create_trabajador_administrador(request):
    if esAdministrador(request):
        if request.method == 'POST':
            form = CreateTrabajadorForm(request.POST, request.FILES)
            if form.is_valid():
                email = form.cleaned_data['email']
                nombre = form.cleaned_data['nombre']
                apellidos = form.cleaned_data['apellidos']
                dni = form.cleaned_data['dni']
                telefono = form.cleaned_data['telefono']
                cualificacion = form.cleaned_data['cualificacion']
                password = nombre[0] + apellidos[0] + dni + "."
                try:
                    vehiculo = Vehiculo.object.get(id=form.cleaned_data['vehiculo'])
                except:
                    vehiculo = None
                if User.objects.filter(username=email):
                    msg_error = "Ya existe un usuario con el correo introducido."
                    return render(request, 'trabajadorAdministradorForm.html', {'form': form, 'msg_error': msg_error})
                else:
                    usuario = User(username=email)
                    usuario.set_password(password)
                    usuario.save()
                    if Persona.objects.filter(telefono=telefono):
                        msg_error = "Ya existe un usuario con el teléfono introducido."
                        usuario.delete()
                        return render(request, 'trabajadorAdministradorForm.html',
                                      {'form': form, 'msg_error': msg_error})
                    if Persona.objects.filter(dni=dni):
                        msg_error = "Ya existe un usuario con el DNI introducido."
                        usuario.delete()
                        return render(request, 'trabajadorAdministradorForm.html',
                                      {'form': form, 'msg_error': msg_error})
                    else:
                        persona = Persona(usuario=usuario, nombre=nombre, apellidos=apellidos, telefono=telefono,
                                          dni=dni)
                        persona.save()
                        trabajador = Trabajador(persona=persona, cualificacion=cualificacion, vehiculo=vehiculo)
                        trabajador.save()
                        return redirect('/administrador/trabajador/')
            else:
                return render(request, 'trabajadorAdministradorForm.html', {'form': form})
        else:
            form = CreateTrabajadorForm()
            return render(request, 'trabajadorAdministradorForm.html', {'form': form})
    else:
        return redirect('/errorPermiso/')


@login_required()
def edit_trabajador_administrador(request, id):
    if esAdministrador(request):
        trabajador = Trabajador.objects.get(id=id)
        if request.method == 'POST':
            form = EditTrabajadorAdministradorForm(request.POST, request.FILES)
            if form.is_valid():
                trabajador.persona.telefono = form.cleaned_data['telefono']
                trabajador.cualificacion = form.cleaned_data['cualificacion']
                vehiculo_id = form.cleaned_data['vehiculo']
                trabajador.vehiculo = None
                if vehiculo_id != "-":
                    trabajador.vehiculo = Vehiculo.objects.get(id=vehiculo_id)
                trabajador.save()
                return redirect('/administrador/trabajador/show/' + str(trabajador.id) + "/")
            else:
                valores = [trabajador.persona.telefono, trabajador.cualificacion]
                items = zip(form, valores)
                return render(request, 'trabajadorAdministradorForm.html',
                              {'form_edit': form, 'trabajador_edit': trabajador, 'items': items})
        else:
            form = EditTrabajadorAdministradorForm()
            valores = [trabajador.persona.telefono, trabajador.cualificacion]
            items = zip(form, valores)
            return render(request, 'trabajadorAdministradorForm.html',
                          {'form_edit': form, 'trabajador_edit': trabajador, 'items': items})
    else:
        return redirect('/errorPermiso/')


@login_required()
def delete_trabajador_administrador(request, id):
    if esAdministrador(request):
        trabajador = Trabajador.objects.get(id=id)
        if len(Servicio.objects.filter(trabajador=trabajador)) != 0:
            msg_error = "No se puede eliminar un trabajador si está asignado a un servicio."
            return render(request, 'trabajadorAdministradorForm.html',
                          {'trabajador': trabajador, 'msg_error': msg_error})
        else:
            trabajador.delete()
            return redirect('/administrador/trabajador/')
    else:
        return redirect('/errorPermiso/')
