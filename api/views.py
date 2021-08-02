from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.request import clone_request
from rest_framework.response import Response
from datetime import datetime
from django.utils.timezone import now
from .serializers import ClienteSerializer, EnderecoSerializer, PontoSerializer, ContratoSerializer, \
    ContratoEventoSerializer
from .models import *


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by('-createdAt')
    serializer_class = ClienteSerializer
    #Não permitir criar cliente com mesmos valores
    def create(self, request, *args, **kwargs):
        serializer = ClienteSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            obj = Cliente.objects.get(name=serializer.validated_data['name'])
            if obj:
                #Reativação
                Cliente.objects.filter(pk=obj.pk).update(removeAt=None)
                return Response(status=status.HTTP_409_CONFLICT)
        except Cliente.DoesNotExist:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = Cliente.objects.all().order_by('-createdAt')

        name = self.request.query_params.get('nome')
        type = self.request.query_params.get('tipo')
        if name is not None:
            queryset = queryset.filter(name=name).order_by('-createdAt')
        elif type is not None:
            queryset = queryset.filter(type=type).order_by('-createdAt')
        return queryset

class EnderecoViewSet(viewsets.ModelViewSet):
    queryset = Endereco.objects.all().order_by('-createdAt')
    serializer_class = EnderecoSerializer

    def create(self, request, *args, **kwargs):
        serializer = EnderecoSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            obj = Endereco.objects.get(public_place=serializer.validated_data['public_place'],
                                       district=serializer.validated_data['district'],
                                       number=serializer.validated_data['number'])
            if obj:
                #Reativação
                Endereco.objects.filter(pk=obj.pk).update(removeAt=None)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Endereco.DoesNotExist:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = Endereco.objects.all().order_by('-createdAt')

        public_place = self.request.query_params.get('logradouro')
        district = self.request.query_params.get('bairro')
        number = self.request.query_params.get('numero')
        if public_place is not None:
            queryset = queryset.filter(public_place=public_place).order_by('-createdAt')
        elif district is not None:
            queryset = queryset.filter(district=district).order_by('-createdAt')
        elif number is not None:
            queryset = queryset.filter(number=number).order_by('-createdAt')
        return queryset


class PontoViewSet(viewsets.ModelViewSet):
    queryset = Ponto.objects.all().order_by('-createdAt')
    serializer_class = PontoSerializer

    def create(self, request, *args, **kwargs):
        serializer = PontoSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        cliente = serializer.validated_data['cliente']
        endereco = serializer.validated_data['endereco']
        obj = Ponto.objects.filter(cliente=cliente, endereco=endereco).first()

        if obj:
            # Reativação do ponto
            Ponto.objects.filter(pk=obj.pk).update(removeAt=None)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if cliente.removeAt != None or endereco.removeAt != None:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = Ponto.objects.all().order_by('-createdAt')

        cliente = self.request.query_params.get('cliente_id')
        endereco = self.request.query_params.get('endereco_id')
        if cliente is not None:
            queryset = queryset.filter(cliente=cliente).order_by('-createdAt')
        elif endereco is not None:
            queryset = queryset.filter(endereco=endereco).order_by('-createdAt')
        return queryset

class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.all().order_by('-createdAt')
    serializer_class = ContratoSerializer

    def create(self, request, *args, **kwargs):
        serializer = ContratoSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            obj = Contrato.objects.get(ponto=serializer.validated_data['ponto'])
            #Reativação
            Contrato.objects.filter(pk=obj.pk).update(removeAt=None)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Contrato.DoesNotExist:
            ponto = Ponto.objects.get(pk=serializer.validated_data['ponto'].pk)
            if ponto.removeAt != None:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.validated_data['status'] = 1
                contrato = serializer.save()
                print(contrato)
                evento = Contrato_Evento(contrato=contrato,statusC=serializer.validated_data['status'])
                evento.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = Contrato.objects.all().order_by('-createdAt')

        cliente = self.request.query_params.get('cliente_id')
        endereco = self.request.query_params.get('endereco_id')
        if cliente is not None:
            queryset = queryset.filter(cliente=cliente).order_by('-createdAt')
        elif endereco is not None:
            queryset = queryset.filter(endereco=endereco).order_by('-createdAt')
        return queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object_or_none()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        obj = Contrato.objects.get(ponto=serializer.validated_data['ponto'])
        statusOBJ = serializer.validated_data['status']

        if obj.status == 3:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif obj.status == 1 and statusOBJ == 3:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            contrato = serializer.save()
            print(contrato)
            evento = Contrato_Evento(contrato=contrato,statusOld=obj.status ,statusC=statusOBJ)
            evento.save()
            print(evento)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def get_object_or_none(self):
        try:
            return self.get_object()
        except Http404:
            if self.request.method == 'PUT':
                self.check_permissions(clone_request(self.request, 'POST'))
            else:
                raise


class ContratoEventoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Contrato_Evento.objects.all().order_by('-createdAt')
    serializer_class = ContratoEventoSerializer

    def get_queryset(self):
        queryset = Contrato_Evento.objects.all().order_by('-createdAt')
        contrato_pk = self.kwargs.get('contrato_pk', None)
        print(contrato_pk)
        if contrato_pk is not None:
            queryset = queryset.filter(contrato=contrato_pk).order_by('-createdAt')
        return queryset

