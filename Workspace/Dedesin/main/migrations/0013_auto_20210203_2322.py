# Generated by Django 3.1.5 on 2021-02-03 22:22

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20210201_2321'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plaga',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
            ],
        ),
        migrations.AlterField(
            model_name='empresa',
            name='cuenta_bancaria',
            field=models.CharField(max_length=22, unique=True, validators=[django.core.validators.RegexValidator('^[A-Za-z]{2}[0-9]{22}$', 'Escribe una cuenta bancaria correcta.')]),
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
            name='SolicitudServicio',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('estado', models.CharField(choices=[('rechazada', 'Rechazada'), ('atendida', 'Atendida'), ('aceptada', 'Aceptada'), ('pendiente', 'Pendiente')], default='pendiente', max_length=9)),
                ('fecha', models.DateField(default=None)),
                ('observaciones', models.TextField()),
                ('plaga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.plaga')),
                ('tratamiento', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.tratamiento')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('estado', models.CharField(choices=[('realizado', 'Realizado'), ('pendiente', 'Pendiente')], default='pendiente', max_length=9)),
                ('observaciones', models.TextField()),
                ('solicitud_servicio', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.solicitudservicio')),
            ],
        ),
    ]
