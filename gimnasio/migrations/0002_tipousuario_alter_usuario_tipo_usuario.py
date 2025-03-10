# Generated by Django 5.1.4 on 2025-01-06 16:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gimnasio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipousuario', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'TipoUsuario',
                'verbose_name_plural': 'TipoUsuarios',
                'db_table': 'TipoUsuarios',
            },
        ),
        migrations.AlterField(
            model_name='usuario',
            name='tipo_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gimnasio.tipousuario'),
        ),
    ]
