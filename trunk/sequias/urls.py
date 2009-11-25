import os
from django.conf.urls.defaults import *
from django.conf import settings
from sequias.models import Encuesta

info = {
         'queryset': Encuesta.objects.all(),
}

urlpatterns = patterns('sequia.sequias.views',
    (r'^index/$', 'consultar'),
    (r'^perdida/$', 'perdidapostrera'),
    (r'^disponibilidad/$', 'disponibilidad'),
    (r'^nutricion/$', 'nutricion'),
    (r'^grafos/$', 'grafo_perdida'),
    (r'^grafos_nutri/$', 'grafo_nutricion'),
    (r'^ajax/municipio/(?P<departamento>\d+)/$', 'get_municipios'),
    (r'^ajax/comunidad/(?P<municipio>\d+)/$', 'get_comunidad'),
    (r'^ajax/entrevista/(?P<comunidad>\d+)/$', 'get_entrevista'),
)
