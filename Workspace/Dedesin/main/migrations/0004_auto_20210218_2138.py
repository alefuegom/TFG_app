# Generated by Django 3.1.5 on 2021-02-18 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210218_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('realizado', 'Realizado')], default='pendiente', max_length=9),
        ),
    ]
