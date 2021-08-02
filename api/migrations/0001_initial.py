# Generated by Django 3.2.3 on 2021-05-19 14:27

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('type', models.IntegerField(choices=[(1, 'Em vigor'), (2, 'Desativado Temporario'), (3, 'Cancelado')], help_text='Tipo do Cliente')),
                ('createdAt', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updateAt', models.DateTimeField(auto_now=True)),
                ('removeAt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.IntegerField(choices=[(1, 'Em vigor'), (2, 'Desativado Temporario'), (3, 'Cancelado')], help_text='Estado do contrato')),
                ('createdAt', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updateAt', models.DateTimeField(auto_now=True)),
                ('removeAt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('public_place', models.CharField(max_length=128)),
                ('district', models.CharField(max_length=128)),
                ('number', models.SmallIntegerField()),
                ('createdAt', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updateAt', models.DateTimeField(auto_now=True)),
                ('removeAt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ponto',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createdAt', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updateAt', models.DateTimeField(auto_now=True)),
                ('removeAt', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pontos_cliente', to='api.cliente', verbose_name='Cliente')),
                ('endereco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pontos_endereco', to='api.endereco', verbose_name='Endereco')),
            ],
        ),
        migrations.CreateModel(
            name='Contrato_Evento',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('statusOld', models.IntegerField(choices=[(1, 'Em vigor'), (2, 'Desativado Temporario'), (3, 'Cancelado')])),
                ('statusC', models.IntegerField(choices=[(1, 'Em vigor'), (2, 'Desativado Temporario'), (3, 'Cancelado')])),
                ('createdAt', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updateAt', models.DateTimeField(auto_now=True)),
                ('removeAt', models.DateTimeField(auto_now=True)),
                ('contrato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evento', to='api.contrato', verbose_name='Contrato')),
            ],
        ),
        migrations.AddField(
            model_name='contrato',
            name='ponto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contrato_ponto', to='api.ponto', verbose_name='Ponto'),
        ),
    ]