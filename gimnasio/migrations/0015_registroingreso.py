# Generated by Django 5.1.4 on 2025-01-21 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gimnasio', '0014_socio_clases_restantes_socio_tipo_mensualidad'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistroIngreso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_ingreso', models.DateTimeField(auto_now_add=True)),
                ('dni_socio', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'RegistroIngreso',
                'verbose_name_plural': 'Registro Ingresos',
                'db_table': 'Registro Ingresos',
            },
        ),
    ]
