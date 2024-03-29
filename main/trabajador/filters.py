import django_filters
from django_filters import DateFilter, ModelChoiceFilter
from django.forms.widgets import TextInput, NumberInput
from ..models import *
ESTADO_SERVICIO = (
        ('Pendiente', 'Pendiente'),
        ('realizado', 'Realizado'),
    )
class ServicioTrabajadorFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(field_name='id', lookup_expr='iexact', widget=NumberInput(attrs={'min': 1}))    
    estado =django_filters.ChoiceFilter(choices=ESTADO_SERVICIO,field_name="estado", label="Estado")
    plaga = django_filters.ModelChoiceFilter(queryset=Plaga.objects.all(), field_name="solicitudServicio__plaga",
                                             label="Plaga")
    fecha = DateFilter(field_name="solicitudServicio__fecha", lookup_expr="iexact", label="Fecha",
                                      widget=TextInput(attrs={'placeholder': 'dd/mm/yyyy'}))

    class Meta:
        model = Servicio
        fields = ["id"]
        exclude = ["id"]