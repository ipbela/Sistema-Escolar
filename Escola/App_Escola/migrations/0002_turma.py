# Generated by Django 5.0.3 on 2024-03-20 13:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Escola', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_turma', models.CharField(max_length=120)),
                ('id_professor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='App_Escola.professor')),
            ],
        ),
    ]