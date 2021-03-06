# Generated by Django 3.1.5 on 2021-02-18 20:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=80)),
                ('dni', models.CharField(max_length=9, unique=True, validators=[django.core.validators.RegexValidator('[0-9]{8}[A-Za-z]{1}', 'Escribe un DNI correcto.')])),
                ('telefono', models.CharField(max_length=9, unique=True, validators=[django.core.validators.RegexValidator('^[0-9]{9}$', 'Escribe un número de teléfono correcto.')])),
                ('usuario', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Plaga',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=50)),
                ('matricula', models.CharField(max_length=7, validators=[django.core.validators.RegexValidator('[0-9]{4}[A-Za-z]{3}', 'Escribe una matrícula correcta.')])),
                ('fecha_matriculacion', models.DateField()),
                ('proxima_revision', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Tratamiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('precio', models.IntegerField()),
                ('abandono', models.BooleanField(default=False)),
                ('horasAbandono', models.IntegerField(default=0)),
                ('plaga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.plaga')),
            ],
        ),
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cualificacion', models.TextField(max_length=254)),
                ('persona', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.persona')),
                ('vehiculo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.vehiculo')),
            ],
        ),
        migrations.CreateModel(
            name='SolicitudServicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('Atendida', 'Atendida'), ('Rechazada', 'Rechazada'), ('Pendiente', 'Pendiente'), ('Aceptada', 'Aceptada')], default='pendiente', max_length=9)),
                ('fecha', models.DateField(default=None, null=True)),
                ('observaciones', models.TextField()),
                ('plaga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.plaga')),
                ('tratamiento', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.tratamiento')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('realizado', 'Realizado'), ('pendiente', 'Pendiente')], default='pendiente', max_length=9)),
                ('observaciones', models.TextField()),
                ('solicitudServicio', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.solicitudservicio')),
                ('trabajador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.trabajador')),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('cif', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z]{1}\\d{7}[a-zA-Z0-9]{1}$', 'Escribe un CIF correcto.')])),
                ('direccion', models.TextField()),
                ('telefono', models.CharField(max_length=9, unique=True, validators=[django.core.validators.RegexValidator('^[0-9]{9}$', 'Escribe un número de teléfono correcto.')])),
                ('cuenta_bancaria', models.CharField(max_length=24, unique=True, validators=[django.core.validators.RegexValidator('^[A-Za-z]{2}[0-9]{22}$', 'Escribe una cuenta bancaria correcta.')])),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.TextField()),
                ('cuenta_bancaria', models.CharField(max_length=24, null=True, validators=[django.core.validators.RegexValidator('^[A-Za-z]{2}[0-9]{22}$', 'Escribe una cuenta bancaria correcta.')])),
                ('persona', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.persona')),
            ],
        ),
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('persona', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.persona')),
            ],
        ),
    ]
