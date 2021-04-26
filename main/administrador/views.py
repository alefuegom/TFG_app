from datetime import datetime, date
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from django.contrib.auth import logout as do_logout
from django.db.models.functions import Lower
from django.http import JsonResponse
from .filters import *
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
                       persona.usuario.username, persona.dni, persona.telefono]
            items = zip(form, valores)
            return render(request, 'perfilAdministrador.html', {'form': form, 'items': items})
    else:
        return redirect('/errorPermiso/')


# CRUD SOLICITUD SERVICIO
@login_required
def list_solicitudServicio_administrador(request):
    if esAdministrador(request):
        solicitudes = SolicitudServicio.objects.all()
        if len(solicitudes) > 0:
            resultado = []
            solicitudServicioFilter = SolicitudServicioAdministradorFilter(request.GET, queryset=solicitudes)
            solicitudes = solicitudServicioFilter.qs
            if len(solicitudes) == 0:
                msg_error = "No existe ninguna solicitud de servicio con los filtros introducidos."
                return render(request, 'solicitudServicioAdministrador.html', {'msg_error':msg_error})
            else:
                for solicitud in solicitudes:
                    try:
                        empresa = Empresa.objects.filter(usuario=solicitud.usuario)[0]
                        resultado.append([solicitud, empresa.nombre])
                    except:
                        persona = Persona.objects.filter(usuario=solicitud.usuario)[0]
                        resultado.append([solicitud, persona.nombre + " " + persona.apellidos])

                paginator = Paginator(resultado, 20)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request, 'solicitudServicioAdministrador.html', {'page_obj': page_obj,
                                                                               'num_solicitudes': len(solicitudes),
                                                                               'solicitudServicioFilter': solicitudServicioFilter})
        else:
            return render(request, 'solicitudServicioAdministrador.html')
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
        usuario = solicitud.usuario
        empresa = None
        cliente = None
        try:
            empresa = Empresa.objects.filter(usuario=usuario)[0]
        except:
            persona = Persona.objects.filter(usuario=usuario)[0]
            cliente = Cliente.objects.filter(persona=persona)[0]
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
                        if empresa:
                            return render(request, 'solicitudServicioAdministradorForm.html',
                                          {'form': form, 'empresa': empresa, 'solicitud_edit': solicitud,
                                           'msg_error': msg_error})
                        if cliente:
                            return render(request, 'solicitudServicioAdministradorForm.html',
                                          {'form': form, 'cliente': cliente, 'solicitud_edit': solicitud,
                                           'msg_error': msg_error})

                else:
                    if cliente:
                        return render(request, 'solicitudServicioAdministradorForm.html',
                                      {'solicitud_edit': solicitud, 'cliente': cliente, 'form': form})
                    if empresa:
                        return render(request, 'solicitudServicioAdministradorForm.html',
                                      {'solicitud_edit': solicitud, 'empresa': empresa, 'form': form})
            else:
                form = EditSolicitudServicioAdministradorForm()
                if cliente:
                    return render(request, 'solicitudServicioAdministradorForm.html',
                                  {'solicitud_edit': solicitud, 'cliente': cliente, 'form': form})
                if empresa:
                    return render(request, 'solicitudServicioAdministradorForm.html',
                                  {'solicitud_edit': solicitud, 'empresa': empresa, 'form': form})
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
        if len(servicios) > 0:
            resultado = []
            servicioFilter = ServicioAdministradorFilter(request.GET, queryset=servicios)
            servicios = servicioFilter.qs
            if len(servicios) == 0:
                msg_error = "No existe ningún servicio con los filtros seleccionados."
                return render(request, "servicioAdministrador.html", {'msg_error':msg_error})
            else:
                for servicio in servicios:
                    try:
                        empresa = Empresa.objects.filter(usuario=servicio.solicitudServicio.usuario)[0]
                        resultado.append([servicio, empresa.nombre])
                    except:
                        persona = Persona.objects.filter(usuario=servicio.solicitudServicio.usuario)[0]
                        resultado.append([servicio, persona.nombre + " " + persona.apellidos])
                paginator = Paginator(resultado, 25)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request, 'servicioAdministrador.html',
                              {'page_obj': page_obj, 'num_servicios': len(servicios), 'servicioFilter': servicioFilter})
        else:
            return render(request, 'servicioAdministrador.html')

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
        usuario = servicio.solicitudServicio.usuario
        empresa = None
        cliente = None
        try:
            empresa = Empresa.objects.filter(usuario=usuario)[0]
        except:
            persona = Persona.objects.filter(usuario=usuario)[0]
            cliente = Cliente.objects.filter(persona=persona)[0]
        if servicio.estado == "Pendiente":
            if request.method == 'POST':
                form = EditServicioAdministradorForm(
                    request.POST, request.FILES)
                if form.is_valid():
                    trabajador = Trabajador.objects.get(
                        id=form.cleaned_data['trabajador'])
                    if trabajador.vehiculo:
                        servicio.trabajador = trabajador
                        print(trabajador.vehiculo)
                        servicio.save()
                        return redirect('/administrador/servicio/')
                    else:
                        msg_error = 'El trabajador asignado debe poseer un vehículo asignado para realizar el servicio.'
                        if cliente:
                            return render(request, 'servicioAdministradorForm.html',
                                          {'servicio_edit': servicio, 'cliente': cliente, 'msg_error': msg_error,
                                           'form': form})
                        if empresa:
                            return render(request, 'servicioAdministradorForm.html',
                                          {'servicio_edit': servicio, 'empresa': empresa, 'msg_error': msg_error,
                                           'form': form})
                else:
                    if cliente:
                        return render(request, 'servicioAdministradorForm.html',
                                      {'servicio_edit': servicio, 'form': form, 'cliente': cliente})
                    if empresa:
                        return render(request, 'servicioAdministradorForm.html',
                                      {'servicio_edit': servicio, 'form': form, 'empresa': empresa})

            else:
                form = EditServicioAdministradorForm()
                if cliente:
                    return render(request, 'servicioAdministradorForm.html',
                                  {'servicio_edit': servicio, 'cliente': cliente,
                                   'form': form})
                if empresa:
                    return render(request, 'servicioAdministradorForm.html',
                                  {'servicio_edit': servicio, 'empresa': empresa,
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
            paginator = Paginator(plagas, 20)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'plagaAdministrador.html', {'page_obj': page_obj, 'num_plagas': len(plagas)})
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
            tratamientoFilter = TratamientoAdministradorFilter(request.GET, queryset=tratamientos)
            tratamientos = tratamientoFilter.qs
            if len(tratamientos) == 0:
                msg_error = "No existe ningún tratamiento con los filtros introducidos."
                return render(request, 'tratamientoAdministrador.html', {'msg_error':msg_error})
            paginator = Paginator(tratamientos, 20)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'tratamientoAdministrador.html',
                          {'page_obj': page_obj,
                           'tratamientoFilter': tratamientoFilter,
                           'num_tratamientos': len(tratamientos)})
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
                    valores = [tratamiento.nombre, tratamiento.precio,
                               tratamiento.abandono, tratamiento.horasAbandono, tratamiento.descripcion]
                    items = zip(form, valores)
                    return render(request, 'tratamientoAdministradorForm.html', {'items': items,
                                                                                 'form_edit': form,
                                                                                 'msg_error': msg_error})

                if abandono and horasAbandono <= 0:
                    msg_error = "Si el tratamiento necesita que se abanone la zona tratada, el valor del tiempo no puede ser 0."
                    valores = [tratamiento.nombre, tratamiento.precio,
                               tratamiento.abandono, tratamiento.horasAbandono, tratamiento.descripcion]
                    items = zip(form, valores)
                    return render(request, 'tratamientoAdministradorForm.html', {'items': items,
                                                                                 'form_edit': form,
                                                                                 'msg_error': msg_error})
                else:
                    tratamiento.nombre = form.cleaned_data['nombre']
                    tratamiento.descripcion = form.cleaned_data['descripcion']
                    tratamiento.abandono = abandono
                    tratamiento.horasAbandono = horasAbandono
                    tratamiento.save()
                    return redirect("/administrador/tratamiento/show/" + str(tratamiento.id) + "/")
            else:
                valores = [tratamiento.nombre, tratamiento.precio,
                           tratamiento.abandono, tratamiento.horasAbandono, tratamiento.descripcion]
                items = zip(form, valores)
                return render(request, 'tratamientoAdministradorForm.html', {'form_edit': form, 'items': items,
                                                                             'tratamiento_edit': tratamiento})
        else:
            form = EditTratamientoAdministradorForm()
            valores = [tratamiento.nombre, tratamiento.precio,
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
        facturas = Factura.objects.all()
        if len(facturas) > 0:
            facturaFilter = FacturaAdministradorFilter(request.GET, queryset=facturas)
            facturas = facturaFilter.qs
            if len(facturas)==0:
                msg_error = "No existe ninguna factura con los filtros seleccionados."
                return render(request, 'facturaAdministrador.html', {'msg_error':msg_error})
            else:
                resultado = []
                for factura in facturas:
                    servicio = Servicio.objects.filter(factura=factura)[0]
                    resultado.append([factura, servicio])
                paginator = Paginator(resultado, 20)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request, 'facturaAdministrador.html', {'page_obj': page_obj,
                                                                     'num_servicios': len(facturas),
                                                                     'facturaFilter': facturaFilter})
        else:
            return render(request, 'facturaAdministrador.html')
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
            vehiculosFilter = VehiculoAdministradorFilter(request.GET, queryset=vehiculos)
            vehiculos = vehiculosFilter.qs
            if len(vehiculos) == 0:
                msg_error = "No existe ningún vehículo con los filtros seleccionados."
                return render(request, 'vehiculoAdministrador.html', {'msg_error':msg_error})
            else:
                vehiculos = vehiculos.order_by('proxima_revision')
                paginator = Paginator(vehiculos, 20)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request, 'vehiculoAdministrador.html',
                              {'page_obj': page_obj, 'vehiculosFilter': vehiculosFilter, 'num_vehiculos': len(vehiculos)})
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
                    try:
                        vehiculo = Vehiculo.objects.filter(
                            matricula=matricula)[0]
                        msg_error = "Ya existe un vehículo con la matrícula introducida "
                        return render(request, 'vehiculoAdministradorForm.html',
                                      {'form': form,
                                       'msg_error': msg_error})
                    except:
                        vehiculo = Vehiculo(marca=marca, modelo=modelo, matricula=matricula,
                                            fecha_matriculacion=fecha_matriculacion,
                                            proxima_revision=proxima_revision)
                        vehiculo.save()
                        return redirect('/administrador/vehiculo')
                except:
                    msg_error = "Introduzca un formato de fecha correcto (dd/mm/yyyy) en el campo de fecha de próxima revisión "
                    return render(request, 'vehiculoAdministradorForm.html',
                                  {'form': form,
                                   'msg_error': msg_error})

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
        if len(trabajadores) > 0:
            trabajadoresFilter = TrabajadorAdministradorFilter(request.GET, queryset=trabajadores)
            trabajadores = trabajadoresFilter.qs
            if len(trabajadores) == 0:
                msg_error = "No existe ningún trabajador con los filtros introducidos."
                return render(request, 'trabajadorAdministrador.html', {'msg_error':msg_error})
            else:
                paginator = Paginator(trabajadores, 20)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request, 'trabajadorAdministrador.html',
                              {'page_obj': page_obj, 'trabajadoresFilter': trabajadoresFilter,
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
                                                                    'trabajador_delete': trabajador_delete})
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
                    vehiculo = Vehiculo.object.get(
                        id=form.cleaned_data['vehiculo'])
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
                        trabajador = Trabajador(
                            persona=persona, cualificacion=cualificacion, vehiculo=vehiculo)
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
                valores = [trabajador.persona.telefono,
                           trabajador.cualificacion]
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


@login_required()
def list_cliente_administrador(request):
    if esAdministrador(request):
        clientes = Cliente.objects.all()
        if len(clientes) == 0:
            return render(request, 'clienteAdministrador.html')
        else:
            clientesFilter = ClienteAdministradorFilter(request.GET, queryset=clientes)
            clientes = clientesFilter.qs
            if len(clientes) == 0:
                msg_error = "No existe ningún cliente con los filtros seleccionados."
                return render(request, 'clienteAdministrador.html', {'msg_error':msg_error})
            paginator = Paginator(clientes, 20)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'clienteAdministrador.html', {'num_clientes': len(clientes),
                                                                 'page_obj': page_obj,
                                                                 'clientesFilter': clientesFilter})
    else:
        return redirect('/errorPermiso/')


@login_required()
def show_cliente_administrador(request, id):
    if esAdministrador(request):
        cliente = Cliente.objects.get(id=id)
        return render(request, 'clienteAdministradorForm.html', {'cliente': cliente})
    else:
        return redirect('/errorPermiso/')


@login_required()
def list_empresa_administrador(request):
    if esAdministrador(request):
        empresas = Empresa.objects.all()
        if len(empresas) == 0:
            return render(request, 'empresaAdministrador.html')
        else:
            empresaFilter = EmpresaAdministradorFilter(request.GET, queryset=empresas)
            empresas = empresaFilter.qs
            if len(empresas) == 0:
                msg_error = "No existe ninguna empresa con los filtros seleccionados."
                return render(request, 'empresaAdministrador.html', {'msg_error': msg_error})
            else:
                paginator = Paginator(empresas, 20)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request, 'empresaAdministrador.html',
                              {'num_empresas': len(empresas), 'page_obj': page_obj,
                               'empresaFilter': empresaFilter})
    else:
        return redirect('/errorPermiso/')


@login_required()
def show_empresa_administrador(request, id):
    if esAdministrador(request):
        empresa = Empresa.objects.get(id=id)
        return render(request, 'empresaAdministradorForm.html', {'empresa': empresa})
    else:
        return redirect('/errorPermiso/')


@login_required()
def list_administrador_administrador(request):
    if esAdministrador(request):
        administradores = Administrador.objects.all()
        if len(administradores) > 0:
            administradoresFilter = AdministradorAdministradorFilter(request.GET, queryset=administradores)
            administradores = administradoresFilter.qs
            if len(administradores) == 0:
                msg_error = "No existe ningún administrador con los filtros introducidos. "
                return render(request, 'administradorAdministrador.html', {'msg_error': msg_error})
            else:
                paginator = Paginator(administradores, 20)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request, 'administradorAdministrador.html',
                              {'page_obj': page_obj, 'num_administradores': len(administradores),
                               'administradoresFilter': administradoresFilter})
        else:
            return render(request, 'administradorAdministrador.html')
    else:
        return redirect('/errorPermiso/')


@login_required()
def show_administrador_administrador(request, id):
    if esAdministrador(request):
        administrador = Administrador.objects.get(id=id)
        return render(request, 'administradorAdministradorForm.html', {'administrador': administrador})
    else:
        return redirect('/errorPermiso/')


@login_required()
def create_administrador_administrador(request):
    if esAdministrador(request):
        if request.method == 'POST':
            form = CreateAdministradorForm(request.POST, request.FILES)
            if form.is_valid():
                nombre = form.cleaned_data['nombre']
                apellidos = form.cleaned_data['apellidos']
                dni = form.cleaned_data['dni']
                telefono = form.cleaned_data['telefono']
                email = form.cleaned_data['email']
                contrasena = form.cleaned_data['contrasena']
                try:
                    User.objects.filter(username=email)[0]
                    msg_error = "Ya existe un usuario con la dirección de correo electrónico introducido."
                    return render(request, 'administradorAdministradorForm.html', {'msg_error': msg_error,
                                                                                   'form': form})
                except:
                    try:
                        Persona.objects.filter(dni=dni)[0]
                        msg_error = "Ya existe un usuario con el DNI introducido."
                        return render(request, 'administradorAdministradorForm.html', {'msg_error': msg_error,
                                                                                       'form': form})
                    except:
                        try:
                            Persona.objects.filter(telefono=telefono)[0]
                            msg_error = "Ya existe un usuario con el telefono introducido."
                            return render(request, 'administradorAdministradorForm.html', {'msg_error': msg_error,
                                                                                           'form': form})
                        except:
                            usuario = User(username=email, password=contrasena)
                            usuario.save()
                            persona = Persona(usuario=usuario, nombre=nombre, apellidos=apellidos, dni=dni,
                                              telefono=telefono)
                            persona.save()
                            administrador = Administrador(persona=persona)
                            administrador.save()
                            return redirect('/administrador/administrador/')
            else:
                return redirect(request, 'administradorAdministradorForm.html', {'form': form})
        else:
            form = CreateAdministradorForm()
            return render(request, 'administradorAdministradorForm.html', {'form': form})
    else:
        return redirect('/errorPermiso/')


@login_required()
def edit_administrador_administrador(request, id):
    if esAdministrador(request):
        administrador = Administrador.objects.get(id=id)
        if request.method == 'POST':
            form = EditAdministradorForm(request.POST, request.FILES)
            if form.is_valid():
                telefono = form.cleaned_data['telefono']
                if telefono != administrador.persona.telefono:
                    try:
                        Persona.objects.filter(telefono=telefono)[0]
                        msg_error = "Ya existe un usuario con el número de telefono introducido."
                        return render(request, 'administradorAdministradorForm.html',
                                      {'msg_error': msg_error, 'form_edit': form, 'administrador_edit': administrador})
                    except:
                        try:
                            Empresa.objects.filter(telefono=telefono)[0]
                            msg_error = "Ya existe un usuario con el número de telefono introducido."
                            return render(request, 'administradorAdministradorForm.html',
                                          {'msg_error': msg_error, 'form_edit': form,
                                           'administrador_edit': administrador})
                        except:
                            administrador.persona.telefono = telefono
                            administrador.save()
                            return redirect('/administrador/administrador/show/' + str(administrador.id))
                else:
                    return redirect('/administrador/administrador/show/' + str(administrador.id))

        else:
            form = EditAdministradorForm()
            return render(request, 'administradorAdministradorForm.html',
                          {'form_edit': form, 'administrador_edit': administrador})
    else:
        return redirect('/errorPermiso/')


@login_required()
def delete_administrador_administrador(request, id):
    if esAdministrador(request):
        administrador = Administrador.objects.get(id=id)
        if len(Administrador.objects.all()) == 1:
            msg_error = "El sistema, al menos, debe tener un administrador."
            return render(request, 'administradorAdministradorForm.html', {'administrador': administrador,
                                                                           'msg_error': msg_error})
        else:
            administrador.delete()
            return redirect('/administrador/administrador')

    else:
        return redirect('/errorPermiso/')

def show_chart_solicitudServicio(request):
    data = [SolicitudServicio.objects.filter(estado="Pendiente").count(),
            SolicitudServicio.objects.filter(estado="Atendida").count(),
            SolicitudServicio.objects.filter(estado="Aceptada").count(),
            SolicitudServicio.objects.filter(estado="Rechazada").count()]
    total_data = 0
    for d in data:
        total_data+=d
    return render(request, 'panelControlAdministrador.html', {'data':data, 'total_data':total_data})