# Generated by Django 5.1.4 on 2025-01-09 13:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gimnasio', '0007_alter_cuota_gimnasio_alter_producto_gimnasio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuota',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
