# Register your models here.
from django.contrib import admin

from .models import *

admin.site.register(Empresa)
admin.site.register(Persona)
admin.site.register(Cliente)
admin.site.register(Vehiculo)
admin.site.register(Trabajador)
admin.site.register(Administrador)
admin.site.register(Plaga)
admin.site.register(Tratamiento)
admin.site.register(SolicitudServicio)
admin.site.register(Factura)
admin.site.register(Servicio)
admin.site.register(Puntuacion)
