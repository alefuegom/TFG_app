import re

from django.core.validators import RegexValidator
from django.db import models

# Con estos patrones podemos validar los campos dni, cif y la cuenta bancaria

DNI_REGEX = RegexValidator(r'^[0-9]{8}[a-z]{1}$', 'Escribe un DNI correcto.')
CIF_REGEX = RegexValidator(r'^[a-zA-Z]{1}\d{7}[a-zA-Z0-9]{1}$', 'Escribe un CIF correcto.')
CUENTA_BANCARIA_REGEX = RegexValidator(r'^[0-9]{20}$', 'Escribe una cuenta bancaria correcta.')
NUMBER_REGEX = RegexValidator(r'^[0-9]{9}$', 'Escribe un número de teléfono correcto.')
CONTRASEÑA_REGEX = RegexValidator(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', 'Escribe una contraseña con al menos 8 caracteres, al menos una letra y un número')


# Create your models here.
class Usuario(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    contraseña = models.CharField(max_length=254, validators=[CONTRASEÑA_REGEX])


class Empresa(models.Model):
    nombre = models.CharField(max_length=50)
    cif = models.CharField(max_length=10, validators=[CIF_REGEX], unique=True)
    direccion = models.TextField()
    telefono = models.BigIntegerField(validators = [NUMBER_REGEX], unique=True)
    cuenta_bancaria = models.CharField(max_length=22,validators=[CUENTA_BANCARIA_REGEX],unique=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)


class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=80)
    dni = models.CharField(max_length=9, validators=[DNI_REGEX],unique=True)
    telefono = models.BigIntegerField(validators = [NUMBER_REGEX],unique=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)


class Cliente(models.Model):
    direccion = models.TextField()
    cuenta_bancaria = models.CharField(max_length=22 ,validators=[CUENTA_BANCARIA_REGEX],unique=True)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)


class Trabajador(models.Model):
    cualificacion = models.TextField(max_length=254)


class Administrador(models.Model):
    administrador = models.OneToOneField(Persona, on_delete=models.CASCADE)
