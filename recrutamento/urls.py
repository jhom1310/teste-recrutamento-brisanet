"""recrutamento URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.views import ClienteViewSet, EnderecoViewSet, PontoViewSet, ContratoViewSet, ContratoEventoViewSet

router_api = routers.DefaultRouter()
router_api.register(r'clientes', ClienteViewSet)
router_api.register(r'enderecos',EnderecoViewSet)
router_api.register(r'pontos', PontoViewSet)
router_api.register(r'contratos', ContratoViewSet)
router_api.register(r'historicos', ContratoEventoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(router_api.urls)),
    url(r'^api/v1/contratos/(?P<contrato_pk>[^/.]+)/historico/$', ContratoEventoViewSet.as_view({'get': 'list'}), name='contrato_evento-list'),
    url(r'^api/v1/clientes/$', ClienteViewSet.as_view({'get': 'list'}))
]
