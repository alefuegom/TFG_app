# Generated by Django 3.1.5 on 2021-02-06 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20210206_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudservicio',
            name='estado',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('Rechazada', 'Rechazada'), ('Aceptada', 'Aceptada'), ('Atendida', 'Atendida')], default='pendiente', max_length=9),
        ),
    ]
