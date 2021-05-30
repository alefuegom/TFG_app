from django import forms
from ..models import *

DNI_REGEX = RegexValidator(r'[0-9]{8}[A-Za-z]{1}', 'Escribe un DNI correcto.')
CIF_REGEX = RegexValidator(
    r'^[a-zA-Z]{1}\d{7}[a-zA-Z0-9]{1}$', 'Escribe un CIF correcto.')
CUENTA_BANCARIA_REGEX = RegexValidator(
    r'^[A-Za-z]{2}[0-9]{22}$', 'Escribe una cuenta bancaria correcta.')
TELEFONO_REGEX = RegexValidator(
    r'^[0-9]{9}$', 'Escribe un número de teléfono correcto.')
CONTRASEÑA_REGEX = RegexValidator(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
                                  'Escribe una contraseña con al menos 8 caracteres, al menos una letra y un número.')


class EditSolicitudServicioClienteForm(forms.Form):
    ESTADO_SOLICITUD = {
        ('Aceptada', 'Aceptada'),
        ('Rechazada', 'Rechazada')
    }
    estado = forms.ChoiceField(choices=ESTADO_SOLICITUD,
                               error_messages={'required': 'El campo estado no puede estar vacío.'})


class EditSolicitudServicioPendienteClienteForm(forms.Form):
    plagas = Plaga.objects.all()
    nombre_plagas = []
    for plaga in plagas:
        nombre_plagas.append([plaga.nombre, plaga.nombre])
    plaga = forms.ChoiceField(choices=nombre_plagas,
                              error_messages={'required': 'El campo plaga no puede estar vacío.'})
    observaciones = forms.CharField()


class CreateSolicitudServicioClienteForm(forms.Form):
    plagas = Plaga.objects.all()
    nombre_plagas = []
    for plaga in plagas:
        nombre_plagas.append([plaga.nombre, plaga.nombre])
    plaga = forms.ChoiceField(choices=nombre_plagas,
                              error_messages={'required': 'El campo plaga no puede estar vacío.'})
    observaciones = forms.CharField()


class EditPerfilClienteForm(forms.Form):
    nombre = forms.CharField(label="Nombre", error_messages={
                             'required': 'El campo nombre no puede estar vacío.'})
    apellidos = forms.CharField(label="Apellidos",
                                error_messages={'required': 'El campo apellidos no puede estar vacío.'})
    dni = forms.CharField(label="DNI", validators=[DNI_REGEX],
                          error_messages={'required': 'El campo DNI no puede estar vacío.'})
    telefono = forms.CharField(label="Telefono", validators=[TELEFONO_REGEX],
                               error_messages={'required': 'El campo teléfono no puede estar vacío.'})
    direccion = forms.CharField(label="Dirección",
                                error_messages={'required': 'El campo dirección no puede estar vacío.'})
    cuentaBancaria = forms.CharField(label="Cuenta bancaria", validators=[
                                     CUENTA_BANCARIA_REGEX], required=False)


class FiltradoFechaSolicitudServicioClienteForm(forms.Form):
    fecha = forms.CharField(
        error_messages={'required': 'El campo fecha no puede estar vacío'})
