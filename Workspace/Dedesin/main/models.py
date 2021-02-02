import re

from django.core.validators import RegexValidator
from django.db import models

# Con estos patrones podemos validar los campos dni, cif y la cuenta bancaria

DNI_REGEX = RegexValidator(r'[0-9]{8}[A-Za-z]{1}', 'Escribe un DNI correcto.')
CIF_REGEX = RegexValidator(r'^[a-zA-Z]{1}\d{7}[a-zA-Z0-9]{1}$', 'Escribe un CIF correcto.')
CUENTA_BANCARIA_REGEX = RegexValidator(r'^[A-Za-z]{2}[0-9]{22}$', 'Escribe una cuenta bancaria correcta.')
TELEFONO_REGEX = RegexValidator(r'^[0-9]{9}$', 'Escribe un número de teléfono correcto.')
CONTRASEÑA_REGEX = RegexValidator(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', 'Escribe una contraseña con al menos 8 caracteres, al menos una letra y un número')

# Create your models here.
class Usuario(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    contraseña = models.CharField(max_length=254, validators=[CONTRASEÑA_REGEX])

    def __str__(self):
        return self.email


class Empresa(models.Model):
    nombre = models.CharField(max_length=50)
    cif = models.CharField(max_length=10, validators=[CIF_REGEX], unique=True)
    direccion = models.TextField()
    telefono = models.CharField(validators = [TELEFONO_REGEX], unique=True, max_length=9)
    cuenta_bancaria = models.CharField(max_length=22,validators=[CUENTA_BANCARIA_REGEX], unique=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.email + "-" + self.cif


class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=80)
    dni = models.CharField(max_length=9, validators=[DNI_REGEX],unique=True)
    telefono = models.CharField(validators = [TELEFONO_REGEX],unique=True,max_length=9)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.email + "-" + self.dni

class Cliente(models.Model):
    direccion = models.TextField()
    cuenta_bancaria = models.CharField(max_length=22 ,validators=[CUENTA_BANCARIA_REGEX],null=True)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)

    def __str__(self):
        return self.persona.usuario.email + "-" + self.persona.dni

class Trabajador(models.Model):
    cualificacion = models.TextField(max_length=254)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, default=None)


    def __str__(self):
        return self.persona.usuario.email + "-" + self.persona.dni

class Administrador(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE,default=None)
    def __str__(self):
        return self.persona.usuario.email + "-" + self.persona.dni
