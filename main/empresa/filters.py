import django_filters
from django_filters import DateFilter, ModelChoiceFilter
from django.forms.widgets import TextInput
from ..models import *

class SolicitudServicioEmpresaFilter(django_filters.FilterSet):
    fecha = DateFilter(field_name="fecha", lookup_expr="iexact", label="Fecha",
                                      widget=TextInput(attrs={'placeholder': 'mm/dd/YYYY'}))
    class Meta:
        model = SolicitudServicio
        fields = ["id", "estado", "plaga"]

ESTADO_SERVICIO = (
    ('Pendiente', 'Pendiente'),
    ('realizado', 'Realizado'),
)
class ServicioEmpresaFilter(django_filters.FilterSet):
    estado =django_filters.ChoiceFilter(choices=ESTADO_SERVICIO,field_name="estado", label="Estado")
    plaga = django_filters.ModelChoiceFilter(queryset=Plaga.objects.all(), field_name="solicitudServicio__plaga",
                                             label="Plaga")
    fecha = DateFilter(field_name="solicitudServicio__fecha", lookup_expr="iexact", label="Fecha",
                                      widget=TextInput(attrs={'placeholder': 'mm/dd/YYYY'}))

    class Meta:
        model = Servicio
        fields = ["id"]
