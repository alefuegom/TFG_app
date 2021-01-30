from django import forms
from django.core.validators import RegexValidator

DNI_REGEX = RegexValidator(r'[0-9]{8}[A-Za-z]{1}', 'Escribe un DNI correcto.')
CIF_REGEX = RegexValidator(r'^[a-zA-Z]{1}\d{7}[a-zA-Z0-9]{1}$', 'Escribe un CIF correcto.')
CUENTA_BANCARIA_REGEX = RegexValidator(r'^[A-Za-z]{2}[0-9]{22}$', 'Escribe una cuenta bancaria correcta.')
TELEFONO_REGEX = RegexValidator(r'^[0-9]{9}$', 'Escribe un número de teléfono correcto.')
CONTRASEÑA_REGEX = RegexValidator(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', 'Escribe una contraseña con al menos 8 caracteres, al menos una letra y un número')

class RegistroClienteForm(forms.Form):
    nombre = forms.CharField()
    apellidos = forms.CharField()
    dni = forms.CharField(validators=[DNI_REGEX])
    email = forms.EmailField()
    contraseña = forms.CharField(widget=forms.PasswordInput, validators= [CONTRASEÑA_REGEX])
    direccion = forms.CharField()
    telefono = forms.IntegerField(validators=[TELEFONO_REGEX])
    cuenta_bancaria = forms.CharField(validators=[CUENTA_BANCARIA_REGEX], required=False)

class InicioSesionForm(forms.Form):
    email = forms.EmailField()
    contraseña = forms.CharField(widget=forms.PasswordInput)