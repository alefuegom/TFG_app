# Generated by Django 3.1.5 on 2021-02-07 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudservicio',
            name='estado',
            field=models.CharField(choices=[('Atendida', 'Atendida'), ('Rechazada', 'Rechazada'), ('Pendiente', 'Pendiente'), ('Aceptada', 'Aceptada')], default='pendiente', max_length=9),
        ),
    ]
