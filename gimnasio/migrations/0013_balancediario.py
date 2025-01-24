# Generated by Django 5.1.4 on 2025-01-16 14:54

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gimnasio', '0012_extras_hora'),
    ]

    operations = [
        migrations.CreateModel(
            name='BalanceDiario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('total_ingresos', models.FloatField(blank=True, null=True)),
                ('total_egresos', models.FloatField(blank=True, null=True)),
                ('balance', models.FloatField(blank=True, null=True)),
                ('gimnasio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balances', to='gimnasio.gimnasio')),
            ],
            options={
                'verbose_name': 'Balance Diario',
                'verbose_name_plural': 'Balance Diarios',
                'db_table': 'Balance Diarios',
            },
        ),
    ]
