from django import forms
from django.views.decorators.cache import cache_control

from ..models import *

DNI_REGEX = RegexValidator(r'[0-9]{8}[A-Za-z]{1}', 'Escribe un DNI correcto.')
TELEFONO_REGEX = RegexValidator(r'^[0-9]{9}$', 'Escribe un número de teléfono correcto.')
MATRICULA_REGEX = RegexValidator(r'[0-9]{4}[A-Za-z]{3}', 'Escribe un matrícula correcta.')
CONTRASEÑA_REGEX = RegexValidator(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
                                  'Escribe una contraseña con al menos 8 caracteres, al menos una letra y un número.')


class EditPerfilAdministrador(forms.Form):
    nombre = forms.CharField(error_messages={'required': 'El campo nombre no puede estar vacío.'})
    apellidos = forms.CharField(error_messages={'required': 'El campo apellidos no puede estar vacío.'})
    email = forms.EmailField(error_messages={'required': 'El campo email no puede estar vacío.'})
    dni = forms.CharField(validators=[DNI_REGEX], error_messages={'required': 'El campo dni no puede estar vacío.'})
    telefono = forms.CharField(validators=[TELEFONO_REGEX],
                               error_messages={'required': 'El campo telefono no puede estar vacío.'})


class EditSolicitudServicioAdministradorForm(forms.Form):
    tratamientos = []
    for tt in Tratamiento.objects.all():
        tratamientos.append([tt.id, tt.nombre])
    trabajadores = []
    for tb in Trabajador.objects.all():
        trabajadores.append([tb.id, tb.persona.nombre + "," + tb.persona.apellidos])
    fecha = forms.CharField(error_messages={'required': 'El campo fecha no puede estar vacío'}, widget=forms.Textarea(attrs={"placeholder": 'dd/mm/yyyy'}))
    tratamiento = forms.ChoiceField(choices=tratamientos,
                                    error_messages={'required': 'El campo tratamiento no puede estar vacío'})


class EditServicioAdministradorForm(forms.Form):
    trabajadores = []
    for tb in Trabajador.objects.all():
        trabajadores.append([tb.id, tb.persona.nombre + "," + tb.persona.apellidos])
    trabajador = forms.ChoiceField(choices=trabajadores,
                                   error_messages={'required': 'El campo trabajador no puede estar vacío'})


class CreatePlagaAdministradorForm(forms.Form):
    nombre = forms.CharField(error_messages={'required': 'El campo nombre no puede estar vacío'})


class CreateTratamientoAdministradorForm(forms.Form):
    nombre = forms.CharField(error_messages={'required': 'El campo nombre no puede estar vacío'})
    nombre_plagas = []
    for p in Plaga.objects.all():
        nombre_plagas.append([p.id, p.nombre])
    plaga = forms.ChoiceField(choices=nombre_plagas)
    precio = forms.IntegerField(error_messages={'required': 'El campo precio no puede estar vacío'}, min_value=0,
                                max_value=99999999)
    abandono = forms.BooleanField(required=False)
    horasAbandono = forms.IntegerField(label='Horas de abandono', min_value=0, max_value=99999999)
    descripcion = forms.CharField(widget=forms.Textarea(attrs={"rows": 3, "cols": 40}), label="Descripción",
                                  error_messages={'required': 'El campo descripción no puede estar vacío'})


class EditTratamientoAdministradorForm(forms.Form):
    nombre = forms.CharField(error_messages={'required': 'El campo nombre no puede estar vacío'})
    precio = forms.IntegerField(error_messages={'required': 'El campo precio no puede estar vacío'}, min_value=0,
                                max_value=99999999)
    abandono = forms.BooleanField(required=False)
    horasAbandono = forms.IntegerField(label='Horas de abandono', min_value=0, max_value=99999999)
    descripcion = forms.CharField(widget=forms.Textarea(attrs={"rows": 3, "cols": 40}), label="Descripción",
                                  error_messages={'required': 'El campo descripción no puede estar vacío'})


class CreateVehiculoAdministradorForm(forms.Form):
    marca = forms.CharField(error_messages={'required': 'El campo marca no puede estar vacío'})
    modelo = forms.CharField(error_messages={'required': 'El campo modelo no puede estar vacío'})
    matricula = forms.CharField(label="Matrícula", max_length=7, min_length=7, validators=[MATRICULA_REGEX])
    fecha_matriculacion = forms.CharField(label="Fecha de matriculación", min_length=10, max_length=10, error_messages={
        'required': 'El campo fecha matriculación no puede estar vacío'}, widget=forms.Textarea(attrs={"placeholder": 'dd/mm/yyyy'}))
    proxima_revision = forms.CharField(label="Fecha de próxima revisión", min_length=10, max_length=10, error_messages={
        'required': 'El campo fecha de próxima revisión no puede estar vacío'}, widget=forms.Textarea(attrs={"placeholder": 'dd/mm/yyyy'}))


class EditVehiculoAdministradorForm(forms.Form):
    proxima_revision = forms.CharField(label="Fecha de próxima revisión", min_length=10, max_length=10, error_messages={
        'required': 'El campo fecha de próxima revisión no puede estar vacío'}, widget=forms.Textarea(attrs={"placeholder": 'dd/mm/yyyy'}))


class CreateTrabajadorForm(forms.Form):
    vehiculos_matricula = [["-", "Ninguno"]]
    for v in Vehiculo.objects.all():
        try:
            trabajador = Trabajador.objects.filter(vehiculo=v)[0]
        except:
            vehiculos_matricula.append([v.id, v.marca + "-" + v.modelo + " (" + v.matricula + ")"])

    nombre = forms.CharField(label="Nombre", error_messages={'required': 'El campo nombre no puede estar vacío.'})
    apellidos = forms.CharField(label="Apellidos",
                                error_messages={'required': 'El campo apellidos no puede estar vacío.'})
    dni = forms.CharField(validators=[DNI_REGEX], label="DNI",
                          error_messages={'required': 'El campo dni no puede estar vacío.'})
    email = forms.EmailField(label="E-mail", error_messages={'required': 'El campo email no puede estar vacío.'})
    telefono = forms.CharField(validators=[TELEFONO_REGEX], label="Teléfono",
                               error_messages={'required': 'El campo teléfono no puede estar vacío.'})
    cualificacion = forms.CharField(label="Cualificación",
                                    error_messages={'required': 'El campo dirección no puede estar vacío.'})
    vehiculo = forms.ChoiceField(choices=vehiculos_matricula, label="Vehículo")


class EditTrabajadorAdministradorForm(forms.Form):
    vehiculos_matricula = [["-", "Ninguno"]]
    vehiculos_asignados = []
    for t in Trabajador.objects.all():
        try:
            if t.vehiculo != None:
                vehiculos_asignados.append(t.vehiculo)
        except:
            pass
    for v in Vehiculo.objects.all():
        if v not in vehiculos_asignados:
            vehiculos_matricula.append([v.id, v.marca + "-" + v.modelo + " (" + v.matricula + ")"])
    telefono = forms.CharField(validators=[TELEFONO_REGEX], label="Teléfono",
                               error_messages={'required': 'El campo teléfono no puede estar vacío.'})
    cualificacion = forms.CharField(label="Cualificación",
                                    error_messages={'required': 'El campo cualificación no puede estar vacío.'})
    vehiculo = forms.ChoiceField(choices=vehiculos_matricula, label="Vehículo")

class CreateAdministradorForm(forms.Form):
    nombre = forms.CharField(error_messages={'required':'El campo nombre no puede estar vacío.'})
    apellidos = forms.CharField(error_messages={'required': 'El campo apellidos no puede estar vacío.'})
    dni = forms.CharField(validators=[DNI_REGEX],error_messages={'required': 'El campo dni no puede estar vacío.'})
    telefono = forms.CharField(label="Teléfono", validators= [TELEFONO_REGEX], error_messages={'required': 'El campo telefono no puede estar vacío.'})
    email = forms.EmailField(label="Dirección de correo electrónico",error_messages={'required': 'El campo email no puede estar vacío.'})
    contrasena = forms.CharField(widget=forms.PasswordInput,label="Contraseña",validators=[CONTRASEÑA_REGEX],error_messages={'required': 'El campo contraseña no puede estar vacío.'})

class EditAdministradorForm(forms.Form):
    telefono = forms.CharField(label ="Teléfono",  validators= [TELEFONO_REGEX], error_messages={'required': 'El campo telefono no puede estar vacío.'})

