from django.contrib import admin
from .models import *

admin.site.register(Cliente)
admin.site.register(Endereco)
admin.site.register(Ponto)
admin.site.register(Contrato)
admin.site.register(Contrato_Evento)
