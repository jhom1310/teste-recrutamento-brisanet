# Generated by Django 3.2.3 on 2021-05-21 15:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210520_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='createdAt',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='type',
            field=models.IntegerField(choices=[(1, 'Juridico'), (2, 'Físico'), (3, 'Especial')]),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='createdAt',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='status',
            field=models.IntegerField(choices=[(1, 'Em vigor'), (2, 'Desativado Temporario'), (3, 'Cancelado')], default=1, help_text='Estado do contrato'),
        ),
        migrations.AlterField(
            model_name='contrato_evento',
            name='createdAt',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='contrato_evento',
            name='statusOld',
            field=models.IntegerField(choices=[(1, 'Em vigor'), (2, 'Desativado Temporario'), (3, 'Cancelado')], default=None),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='createdAt',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='ponto',
            name='createdAt',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterUniqueTogether(
            name='endereco',
            unique_together=set(),
        ),
    ]
