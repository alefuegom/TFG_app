from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

# Con estos patrones podemos validar los campos dni, cif y la cuenta bancaria

DNI_REGEX = RegexValidator(r'[0-9]{8}[A-Za-z]{1}', 'Escribe un DNI correcto.')
MATRICULA_REGEX = RegexValidator(r'[0-9]{4}[A-Za-z]{3}', 'Escribe una matrícula correcta.')
CIF_REGEX = RegexValidator(r'^[a-zA-Z]{1}\d{7}[a-zA-Z0-9]{1}$', 'Escribe un CIF correcto.')
CUENTA_BANCARIA_REGEX = RegexValidator(r'^[A-Za-z]{2}[0-9]{22}$', 'Escribe una cuenta bancaria correcta.')
TELEFONO_REGEX = RegexValidator(r'^[0-9]{9}$', 'Escribe un número de teléfono correcto.')
CONTRASEÑA_REGEX = RegexValidator(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
                                  'Escribe una contraseña con al menos 8 caracteres, al menos una letra y un número')


class Empresa(models.Model):
    nombre = models.CharField(max_length=50)
    cif = models.CharField(max_length=10, validators=[CIF_REGEX], unique=True)
    direccion = models.TextField()
    telefono = models.CharField(validators=[TELEFONO_REGEX], unique=True, max_length=9)
    cuenta_bancaria = models.CharField(max_length=24, validators=[CUENTA_BANCARIA_REGEX], unique=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + "-" + self.cif


class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=80)
    dni = models.CharField(max_length=9, validators=[DNI_REGEX], unique=True)
    telefono = models.CharField(validators=[TELEFONO_REGEX], unique=True, max_length=9)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.nombre + "," + self.apellidos + "-" + self.dni


class Cliente(models.Model):
    direccion = models.TextField()
    cuenta_bancaria = models.CharField(max_length=24, validators=[CUENTA_BANCARIA_REGEX], null=True)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)

    def __str__(self):
        return self.persona.nombre + "," + self.persona.apellidos + "-" + self.persona.dni


class Vehiculo(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    matricula = models.CharField(max_length=7, validators=[MATRICULA_REGEX])
    fecha_matriculacion = models.DateField()
    proxima_revision = models.DateField()

    def __str__(self):
        return self.marca + "-" + self.modelo + "(" + self.matricula + ")"


class Trabajador(models.Model):
    cualificacion = models.TextField(max_length=254)
    vehiculo = models.OneToOneField(Vehiculo, on_delete=models.CASCADE)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.persona.nombre + "," + self.persona.apellidos + "-" + self.persona.dni


class Administrador(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.persona.nombre + "," + self.persona.apellidos + "-" + self.persona.dni


class Plaga(models.Model):
    nombre = models.CharField(max_length=60)

    def __str__(self):
        return self.nombre


class Tratamiento(models.Model):
    nombre = models.CharField(max_length=100, blank=False)
    descripcion = models.TextField()
    precio = models.FloatField()
    abandono = models.BooleanField(default=False)
    horasAbandono = models.IntegerField(default=0)
    plaga = models.ForeignKey(Plaga, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + "-" + self.plaga.nombre


ESTADO_SOLICITUD = {
    ('Pendiente', 'Pendiente'),
    ('Atendida', 'Atendida'),
    ('Aceptada', 'Aceptada'),
    ('Rechazada', 'Rechazada')
}


class SolicitudServicio(models.Model):
    estado = models.CharField(choices=ESTADO_SOLICITUD, default='pendiente', max_length=9)
    fecha = models.DateField(default=None, null=True)
    observaciones = models.TextField()
    tratamiento = models.ForeignKey(Tratamiento, on_delete=models.CASCADE, default=None, null=True)
    plaga = models.ForeignKey(Plaga, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + "-" + self.usuario.username + " (" + self.estado + ")"


ESTADO_SERVICIO = {
    ('pendiente', 'Pendiente'),
    ('realizado', 'Realizado')
}


class Factura(models.Model):
    fecha_expedicion = models.DateField()
    emisor = models.CharField(default="Dedesin SL",max_length=50)
    receptor = models.CharField(max_length=50)
    descripcion = models.TextField()
    importe = models.FloatField()
    tipo_impositivo = models.FloatField(default=21)
    fecha_operaciones = models.DateField()

    def __str__(self):
        return str(self.id) + " - " + self.receptor + "[ " + self.descripcion + " ]"


class Servicio(models.Model):
    estado = models.CharField(choices=ESTADO_SERVICIO, default='pendiente', max_length=9)
    observaciones = models.TextField()
    solicitudServicio = models.OneToOneField(SolicitudServicio, on_delete=models.CASCADE)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE, null=True)
    factura = models.OneToOneField(Factura,  on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return str(self.id) + "-" + self.estado + " [" + str(self.solicitudServicio.id) + "]"
