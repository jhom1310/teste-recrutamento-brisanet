from rest_framework import serializers
from rest_framework.fields import ChoiceField
from rest_framework.reverse import reverse

from .models import *

class DisplayNameWritableField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        self.html_cutoff = kwargs.pop('html_cutoff', self.html_cutoff)
        self.html_cutoff_text = kwargs.pop('html_cutoff_text', self.html_cutoff_text)

        self.allow_blank = kwargs.pop('allow_blank', False)
        super(ChoiceField, self).__init__(**kwargs)

    def to_representation(self, value):
        return self.choices.get(value, value)

    def bind(self, field_name, parent):
        super().bind(field_name, parent)
        self.choices = parent.Meta.model._meta.get_field(field_name).choices

class ClienteSerializer(serializers.ModelSerializer):
    type = DisplayNameWritableField()
    class Meta:
        model = Cliente
        fields = ['name', 'type']

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ['public_place', 'district', 'number']

class PontoSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.name', read_only=True)
    cliente_tipo = serializers.CharField(source='cliente.get_type_display', read_only=True)
    endereco_logradouro = serializers.CharField(source='endereco.public_place', read_only=True)
    endereco_bairro = serializers.CharField(source='endereco.district', read_only=True)
    endereco_numero = serializers.IntegerField(source='endereco.number', read_only=True)
    class Meta:
        model = Ponto
        fields = ['cliente', 'cliente_nome', 'cliente_tipo', 'endereco', 'endereco_logradouro',
                  'endereco_bairro', 'endereco_numero']

class ContratoSerializer(serializers.ModelSerializer):
    cliente_id = serializers.UUIDField(source='ponto.cliente.id', read_only=True)
    cliente_nome = serializers.CharField(source='ponto.cliente.name', read_only=True)
    cliente_tipo = serializers.CharField(source='ponto.cliente.get_type_display', read_only=True)
    endereco_id = serializers.UUIDField(source='ponto.endereco.id', read_only=True)
    endereco_logradouro = serializers.CharField(source='ponto.endereco.public_place', read_only=True)
    endereco_bairro = serializers.CharField(source='ponto.endereco.district', read_only=True)
    endereco_numero = serializers.IntegerField(source='ponto.endereco.number', read_only=True)

    class Meta:
        model = Contrato
        fields = ['cliente_id','cliente_nome','cliente_tipo','endereco_id','endereco_logradouro',
                  'endereco_bairro','endereco_numero', 'ponto', 'status']
        extra_kwargs = {
            'ponto': {'write_only': True},
            'status': {'write_only': True}
        }

class ContratoEventoSerializer(serializers.ModelSerializer):
    statusOld = DisplayNameWritableField()
    statusC = DisplayNameWritableField()
    class Meta:
        model = Contrato_Evento
        fields = ['id', 'createdAt','statusOld', 'statusC']