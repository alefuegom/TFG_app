from django import forms
from django.core.validators import RegexValidator

DNI_REGEX = RegexValidator(r'[0-9]{8}[A-Za-z]{1}', 'Escribe un DNI correcto.')
CIF_REGEX = RegexValidator(r'^[a-zA-Z]{1}\d{7}[a-zA-Z0-9]{1}$', 'Escribe un CIF correcto.')
CUENTA_BANCARIA_REGEX = RegexValidator(r'^[A-Za-z]{2}[0-9]{22}$', 'Escribe una cuenta bancaria correcta.')
TELEFONO_REGEX = RegexValidator(r'^[0-9]{9}$', 'Escribe un número de teléfono correcto.')
CONTRASEÑA_REGEX = RegexValidator(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,15}',
                                  'Escriba una contraseña entre 8 y 15 caracteres, al menos una letra minúscula, otra mayúscula, un número y un carácter especial.')


class RegistroClienteForm(forms.Form):
    nombre = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    apellidos = forms.CharField(label="Apellidos",  widget=forms.TextInput(attrs={'placeholder': 'Apellidos'}))
    dni = forms.CharField(validators=[DNI_REGEX], label="DNI",  widget=forms.TextInput(attrs={'placeholder': 'DNI'}))
    email = forms.EmailField(label="E-mail",  widget=forms.TextInput(attrs={'placeholder': 'E-mail'}))
    contraseña = forms.CharField(validators=[CONTRASEÑA_REGEX], label="Contraseña", widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
    direccion = forms.CharField(label="Dirección",  widget=forms.TextInput(attrs={'placeholder': 'Dirección'}))
    telefono = forms.CharField(validators=[TELEFONO_REGEX], label="Teléfono",  widget=forms.TextInput(attrs={'placeholder': 'Teléfono'}))
    cuenta_bancaria = forms.CharField(validators=[CUENTA_BANCARIA_REGEX], widget=forms.TextInput(attrs={'placeholder': 'Cuenta Bancaria'}), required=False, label="Cuenta bancaria")


class RegistroEmpresaForm(forms.Form):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nombre de la empresa'}), label="Nombre",)
    CIF = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'CIF'}), validators=[CIF_REGEX],label="CIF")
    email = forms.EmailField(label="E-mail", widget=forms.TextInput(attrs={'placeholder': 'E-mail'}))
    contraseña = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}), validators=[CONTRASEÑA_REGEX], label="Contraseña")
    telefono = forms.CharField(validators=[TELEFONO_REGEX], label="Teléfono", widget=forms.TextInput(attrs={'placeholder': 'Teléfono'}))
    cuenta_bancaria = forms.CharField(validators=[CUENTA_BANCARIA_REGEX], required=True,label="Cuenta bancaria", widget=forms.TextInput(attrs={'placeholder': 'Cuenta bancaria'}))
    direccion = forms.CharField(label="Dirección",  widget=forms.TextInput(attrs={'placeholder': 'Dirección'}))


class InicioSesionForm(forms.Form):
    email = forms.EmailField(label="E-mail",  widget=forms.TextInput(attrs={'placeholder': 'E-mail'}))
    contraseña = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
