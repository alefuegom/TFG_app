from django import forms
from ..models import *

DNI_REGEX = RegexValidator(r'[0-9]{8}[A-Za-z]{1}', 'Escribe un DNI correcto.')
TELEFONO_REGEX = RegexValidator(r'^[0-9]{9}$', 'Escribe un número de teléfono correcto.')


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
    fecha = forms.CharField(error_messages={'required': 'El campo fecha no puede estar vacío'})
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
