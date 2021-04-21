import django_filters
from django_filters import DateFilter, ModelChoiceFilter
from django.forms.widgets import TextInput
from ..models import *


class SolicitudServicioAdministradorFilter(django_filters.FilterSet):
    fecha = DateFilter(field_name="fecha", lookup_expr="iexact", label="Fecha",
                                      widget=TextInput(attrs={'placeholder': 'mm/dd/YYYY'}))
    id = django_filters.NumberFilter(field_name='id', lookup_expr='iexact')

    class Meta:
        model = SolicitudServicio
        fields = "__all__"
        exclude = ['observaciones', 'usuario', 'tratamiento']

ESTADO_SERVICIO = (
        ('Pendiente', 'Pendiente'),
        ('realizado', 'Realizado'),
    )

class ServicioAdministradorFilter(django_filters.FilterSet):
    fecha = django_filters.DateFilter(field_name="solicitudServicio__fecha", label="Fecha",
                                      widget=TextInput(attrs={'placeholder': 'mm/dd/YYYY'}))
    plaga = django_filters.ModelChoiceFilter(queryset=Plaga.objects.all(), field_name="solicitudServicio__plaga",
                                             label="Plaga")
    estado =django_filters.ChoiceFilter(choices=ESTADO_SERVICIO,field_name="estado", label="Estado")
    class Meta:
        model = Servicio
        fields = ["id", "trabajador"]


class FacturaAdministradorFilter(django_filters.FilterSet):
    fecha_expedicion = django_filters.DateFilter(field_name="fecha_expedicion", label="Fecha",
                                      widget=TextInput(attrs={'placeholder': 'mm/dd/YYYY'}))
    receptor = django_filters.CharFilter(field_name='receptor', lookup_expr='icontains', label="Receptor")

    class Meta:
        model = Factura
        fields = ["id"]

class TratamientoAdministradorFilter(django_filters.FilterSet):
    plaga = django_filters.ModelChoiceFilter(queryset=Plaga.objects.all(), field_name="plaga",
                                             label="Plaga")
    nombre = django_filters.CharFilter(field_name='nombre', lookup_expr='icontains', label="Nombre")
    class Meta:
        model = Factura
        fields = ["id"]

class ClienteAdministradorFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(field_name='persona__nombre', lookup_expr='icontains', label="Nombre")
    apellidos = django_filters.CharFilter(field_name='persona__apellidos', lookup_expr='icontains', label="Apellidos")
    dni = django_filters.CharFilter(field_name='persona__dni', lookup_expr='icontains', label="DNI")
    class Meta:
        model = Cliente
        fields = ["id"]
        exclude = ["id"]

class EmpresaAdministradorFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(field_name='nombre', lookup_expr='icontains', label="Nombre")
    CIF = django_filters.CharFilter(field_name='cif', lookup_expr='icontains', label="CIF")

    class Meta:
        model = Empresa
        fields = ["id"]
        exclude = ["id"]

class TrabajadorAdministradorFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(field_name='persona__nombre', lookup_expr='icontains', label="Nombre")
    apellidos = django_filters.CharFilter(field_name='persona__apellidos', lookup_expr='icontains', label="Apellidos")
    dni = django_filters.CharFilter(field_name='persona__dni', lookup_expr='icontains', label="DNI")
    class Meta:
        model = Trabajador
        fields = ["id"]
        exclude = ["id"]

class VehiculoAdministradorFilter(django_filters.FilterSet):
    matricula = django_filters.CharFilter(field_name='matricula', lookup_expr='icontains', label="Matrícula")
    marca = django_filters.CharFilter(field_name='marca', lookup_expr='icontains', label="Marca")

    class Meta:
        model = Vehiculo
        fields = ["id"]
        exclude = ["id"]

class AdministradorAdministradorFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(field_name='persona__nombre', lookup_expr='icontains', label="Nombre")
    apellidos = django_filters.CharFilter(field_name='persona__apellidos', lookup_expr='icontains', label="Apellidos")
    dni = django_filters.CharFilter(field_name='persona__dni', lookup_expr='icontains', label="DNI")
    class Meta:
        model = Administrador
        fields = ["id"]
        exclude = ["id"]

