 # -*- coding: UTF-8 -*-
 
from django.shortcuts import render_to_response
from sequia.sequias.models import Encuesta
from forms import *
from lugar.models import *
from django.conf import settings
from django.db.models import Sum, Count, Avg
from django.utils import simplejson
from decimal import Decimal
from django.views.generic.simple import direct_to_template
from django.http import HttpResponse, HttpResponseBadRequest
from decorators import session_required

def index(request):
    return render_to_response('base.html')

def consultar(request):
    if request.method=='POST':
        mensaje = None
        form = SequiaForm(request.POST)
        if form.is_valid():
            request.session['fecha_inicio'] = form.cleaned_data['fecha_inicio']
            request.session['fecha_final'] = form.cleaned_data['fecha_final'] 
            request.session['departamento'] = form.cleaned_data['departamento']
            try:
                municipio = Municipio.objects.get(id=form.cleaned_data['municipio']) 
            except:
                municipio = None
            try:
                comunidad = Comunidad.objects.get(id=form.cleaned_data['comunidad']) 
            except:
                comunidad = None
            try:
                entrevistado = Entrevistado.objects.get(id=form.cleaned_data['entrevistado'])
            except:
                entrevistado= None
            request.session['municipio'] = municipio 
            request.session['comunidad'] = comunidad
            request.session['entrevistado'] = entrevistado
            mensaje = "Ahora puede seleccionar los datos con los botones de la derecha"
            request.session['activo'] = True 
    else:
        form = SequiaForm()
        mensaje = "" 
    dict = {'form': form, 'mensaje': mensaje,'user': request.user}
    return direct_to_template(request, 'encuesta/index.html', dict)

def get_municipios(request, departamento):
    municipios = Municipio.objects.filter(departamento = departamento)
    lista = [(municipio.id, municipio.nombre) for municipio in municipios]
    return HttpResponse(simplejson.dumps(lista), mimetype='application/javascript')

def get_comunidad(request, municipio):
    comunidades = Comunidad.objects.filter(municipio = municipio )
    lista = [(comunidad.id, comunidad.nombre) for comunidad in comunidades]
    return HttpResponse(simplejson.dumps(lista), mimetype='application/javascript')

def get_entrevista(request, comunidad):
    entrevistados = Entrevistado.objects.filter(comunidad = comunidad )
    lista = [(entrevista.id, entrevista.nombre) for entrevista in entrevistados]
    return HttpResponse(simplejson.dumps(lista), mimetype='application/javascript')
