import django_filters
from django_filters import DateFilter, ModelChoiceFilter
from django.forms.widgets import NumberInput, TextInput
from ..models import *

ESTADO_SOLICITUD = (
        ('Pendiente', 'Pendiente'),
        ('Atendida', 'Atendida'),
        ('Aceptada', 'Aceptada'),
        ('Rechazada', 'Rechazada'),
    )

class SolicitudServicioAdministradorFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(field_name='id', lookup_expr='iexact', widget=NumberInput(attrs={'min': 1}))
    estado =django_filters.ChoiceFilter(choices=ESTADO_SOLICITUD,field_name="estado", label="Estado")
    fecha = DateFilter(field_name="fecha", lookup_expr="iexact", label="Fecha",
                                      widget=TextInput(attrs={'placeholder': 'dd/mm/yyyy'}))
    plaga = django_filters.ModelChoiceFilter(queryset=Plaga.objects.all(), field_name="plaga",
                                             label="Plaga")
    class Meta:
        model = SolicitudServicio
        fields = "__all__"
        exclude = ['id','plaga', 'estado', 'fecha','observaciones', 'usuario', 'tratamiento']

ESTADO_SERVICIO = (
        ('Pendiente', 'Pendiente'),
        ('realizado', 'Realizado'),
    )

class ServicioAdministradorFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(field_name='id', lookup_expr='iexact', widget=NumberInput(attrs={'min': 1}))
    estado =django_filters.ChoiceFilter(choices=ESTADO_SERVICIO,field_name="estado", label="Estado")
    fecha = django_filters.DateFilter(field_name="solicitudServicio__fecha", label="Fecha",
                                      widget=TextInput(attrs={'placeholder': 'dd/mm/yyyy'}))
    plaga = django_filters.ModelChoiceFilter(queryset=Plaga.objects.all(), field_name="solicitudServicio__plaga",
                                             label="Plaga")
    trabajador = django_filters.ModelChoiceFilter(queryset=Trabajador.objects.all(), field_name="trabajador",
                                             label="Trabajador")
    class Meta:
        model = Servicio
        fields = ["trabajador"]
        exclude=['trabajador']


class FacturaAdministradorFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(field_name='id', lookup_expr='iexact', widget=NumberInput(attrs={'min': 1}))
    fecha_expedicion = django_filters.DateFilter(field_name="fecha_expedicion", label="Fecha",
                                      widget=TextInput(attrs={'placeholder': 'dd/mm/yyyy'}))
    receptor = django_filters.CharFilter(field_name='receptor', lookup_expr='icontains', label="Receptor")

    class Meta:
        model = Factura
        fields = ["id"]
        exclude = ["id"]

class TratamientoAdministradorFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(field_name='id', lookup_expr='iexact', widget=NumberInput(attrs={'min': 1}))
    plaga = django_filters.ModelChoiceFilter(queryset=Plaga.objects.all(), field_name="plaga",
                                             label="Plaga")
    nombre = django_filters.CharFilter(field_name='nombre', lookup_expr='icontains', label="Nombre")
    class Meta:
        model = Factura
        fields = ["id"]
        exclude = ["id"]


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

