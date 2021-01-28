from django import forms


class RegistroClienteForm(forms.Form):
    nombre = forms.CharField()
    apellidos = forms.CharField()
    dni = forms.CharField()
    email = forms.EmailField()
    contraseña = forms.CharField()
    direccion = forms.CharField()
    telefono = forms.IntegerField()
    cuenta_bancaria = forms.CharField()

class InicioSesionForm(forms.Form):
    email = forms.EmailField()
    contraseña = forms.CharField()