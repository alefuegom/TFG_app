from django import forms
from django.core.validators import RegexValidator

DNI_REGEX = RegexValidator(r'[0-9]{8}[A-Za-z]{1}', 'Escribe un DNI correcto.')
CUENTA_BANCARIA_REGEX = RegexValidator(r'^[A-Za-z]{2}[0-9]{22}$', 'Escribe una cuenta bancaria correcta.')
TELEFONO_REGEX = RegexValidator(r'^[0-9]{9}$', 'Escribe un número de teléfono correcto.')


class EditServicioTrabajadorForm(forms.Form):
    observaciones = forms.CharField(error_messages={'required': 'El campo observaciones no puede estar vacío.'})


class EditPerfilTrabajadorForm(forms.Form):
    nombre = forms.CharField(label="Nombre", error_messages={'required': 'El campo nombre no puede estar vacío.'})
    apellidos = forms.CharField(label="Apellidos",
                                error_messages={'required': 'El campo apellidos no puede estar vacío.'})
    dni = forms.CharField(label="DNI", validators=[DNI_REGEX],
                          error_messages={'required': 'El campo DNI no puede estar vacío.'})
    telefono = forms.CharField(label="Telefono", validators=[TELEFONO_REGEX],
                               error_messages={'required': 'El campo teléfono no puede estar vacío.'})
    cualificacion = forms.CharField(label="Cualificación", error_messages={'required': 'El campo dirección no puede estar vacío.'})
