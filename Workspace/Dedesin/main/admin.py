# Register your models here.
from django.contrib import admin

from .models import *

admin.site.register(Usuario)
admin.site.register(Empresa)
admin.site.register(Persona)
admin.site.register(Cliente)
admin.site.register(Trabajador)
admin.site.register(Administrador)
