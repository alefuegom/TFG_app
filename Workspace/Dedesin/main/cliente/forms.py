from django import forms
from ..models import *


class EditSolicitudServicioClienteForm(forms.Form):
    ESTADO_SOLICITUD = {
        ('Aceptada', 'Aceptada'),
        ('Rechazada', 'Rechazada')
    }
    estado = forms.ChoiceField(choices=ESTADO_SOLICITUD)


class CreateSolicitudServicioClienteForm(forms.Form):
    plagas = Plaga.objects.all()
    nombre_plagas = []
    for plaga in plagas:
        nombre_plagas.append([plaga.nombre,plaga.nombre])
    plaga = forms.ChoiceField(choices=nombre_plagas)
    observaciones = forms.CharField()
