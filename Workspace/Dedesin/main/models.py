from django.db import models


# Create your models here.
class Usuario(models.Model):
    email = models.EmailField(max_length=254)
    contraseña = models.CharField(max_length=254)


class Empresa(models.Model):
    nombre = models.CharField(max_length=50)
    cif = models.CharField(max_length=10)
    direccion = models.TextField()
    telefono = models.BigIntegerField()
    cuenta_bancaria = models.CharField(max_length=22)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)


class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=80)
    dni = models.CharField(max_length=9)
    telefono = models.BigIntegerField()
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)


class Cliente(models.Model):
    direccion = models.TextField()
    cuenta_bancaria = models.CharField(max_length=22)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)


class Trabajador(models.Model):
    cualificacion = models.TextField(max_length=254)


class Administrador(models.Model):
    administrador = models.OneToOneField(Persona, on_delete=models.CASCADE)
