# Generated by Django 5.1.4 on 2025-01-06 19:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gimnasio', '0004_egreso_extras'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuota',
            name='gimnasio',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='Cuota', to='gimnasio.gimnasio'),
        ),
        migrations.AddField(
            model_name='egreso',
            name='gimnasio',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='egreso', to='gimnasio.gimnasio'),
        ),
        migrations.AddField(
            model_name='extras',
            name='gimnasio',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='extras', to='gimnasio.gimnasio'),
        ),
        migrations.AddField(
            model_name='ingresos',
            name='gimnasio',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='ingresos', to='gimnasio.gimnasio'),
        ),
        migrations.AddField(
            model_name='producto',
            name='gimnasio',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='Producto', to='gimnasio.gimnasio'),
        ),
        migrations.AddField(
            model_name='socio',
            name='gimnasio',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='socios', to='gimnasio.gimnasio'),
        ),
        migrations.AddField(
            model_name='venta',
            name='gimnasio',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='Venta', to='gimnasio.gimnasio'),
        ),
    ]
