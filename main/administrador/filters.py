import django_filters
from django_filters import DateFilter
from ..models import *

class SolicitudServicioFilter(django_filters.FilterSet):
    fecha = DateFilter(field_name="fecha", lookup_expr="iexact")
    class Meta:
        model = SolicitudServicio
        fields = "__all__"
        exclude=['observaciones', 'usuario']
