from datetime import datetime
from django.utils.timezone import now
import uuid

from django.db import models

class Cliente(models.Model):

    TYPE_CHOICES = (
        (1, 'Juridico'),
        (2, 'Físico'),
        (3, 'Especial'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    type = models.IntegerField(choices=TYPE_CHOICES)
    createdAt = models.DateTimeField(default=now, blank=True)
    updateAt = models.DateTimeField(auto_now=True)
    removeAt = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.name) +' - '+ str(self.get_type_display())

    def get_cliente_id(self):
        return self.id

class Endereco(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_place = models.CharField(max_length=128)
    district = models.CharField(max_length=128)
    number = models.SmallIntegerField()
    createdAt = models.DateTimeField(default=now, blank=True)
    updateAt = models.DateTimeField(auto_now=True)
    removeAt = models.DateTimeField(blank=True, null=True)



class Ponto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente', related_name='pontos_cliente')
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, verbose_name='Endereco', related_name='pontos_endereco')
    createdAt = models.DateTimeField(default=now, blank=True)
    updateAt = models.DateTimeField(auto_now=True)
    removeAt = models.DateTimeField(blank=True, null=True)

class Contrato(models.Model):
    STATUS_CHOICES = (
        (1, 'Em vigor'),
        (2, 'Desativado Temporario'),
        (3, 'Cancelado')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ponto = models.ForeignKey(Ponto, on_delete=models.CASCADE, verbose_name='Ponto', related_name='contrato_ponto')
    status = models.IntegerField(choices=STATUS_CHOICES, help_text='Estado do contrato', default=1)
    createdAt = models.DateTimeField(default=now, blank=True)
    updateAt = models.DateTimeField(auto_now=True)
    removeAt = models.DateTimeField(blank=True, null=True)

class Contrato_Evento(models.Model):
    STATUS_CHOICES = (
        (1, 'Em vigor'),
        (2, 'Desativado Temporario'),
        (3, 'Cancelado')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, verbose_name='Contrato', related_name='evento')
    statusOld = models.IntegerField(choices=STATUS_CHOICES, default=None, null=True, blank=True)
    statusC = models.IntegerField(choices=STATUS_CHOICES)
    createdAt = models.DateTimeField(default=now, blank=True)
    updateAt = models.DateTimeField(auto_now=True)
    removeAt = models.DateTimeField(blank=True, null=True)