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
from django.views.decorators.cache import cache_page
from django.template.loader import get_template
from django.template import Context

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

#Vista para la perdida de la cosecha primera


def perdidapostrera(request):
    fecha1=request.session['fecha_inicio']
    fecha2=request.session['fecha_final']
    if request.session['comunidad']:
        com = request.session['comunidad'].id
        perdida = Encuesta.objects.filter(fecha=fecha1,fecha=fecha2).filter(entrevistado__comunidad__id=com)
    elif request.session['municipio']:
        mun = request.session['municipio'].id
        perdida = Encuesta.objects.filter(fecha=fecha1,fecha=fecha2).filter(entrevistado__comunidad__municipio__id=mun)
    elif request.session['departamento']:
        dep = request.session['departamento'].id
        perdida = Encuesta.objects.filter(fecha=fecha1,fecha=fecha2).filter(entrevistado__comunidad__municipio__departamento__id=dep)
    elif request.session['entrevistado']:
        entre = request.session['entrevistado'].id
        perdida = Encuesta.objects.filter(fecha=fecha1,fecha=fecha2).filter(entrevistado__nombre=entre)
    else:
        perdida = Encuesta.objects.all()
        
    casos = perdida.count()
    #TODO: Sumatorias de maiz,frijol,sorgo primera de area_sembrada
    arroz_sembrada = perdida.filter(primera__producto__id=1).aggregate(Sum('primera__area_sembrada'))
    frijol_sembrada = perdida.filter(primera__producto__id=2).aggregate(Sum('primera__area_sembrada'))
    maiz_sembrada = perdida.filter(primera__producto__id=3).aggregate(Sum('primera__area_sembrada'))
    #TODO: area cosechada
    arroz_cosechada = perdida.filter(primera__producto__id=1).aggregate(Sum('primera__area_cosechada'))
    frijol_cosechada = perdida.filter(primera__producto__id=2).aggregate(Sum('primera__area_cosechada'))
    maiz_cosechada = perdida.filter(primera__producto__id=3).aggregate(Sum('primera__area_cosechada'))
    #TODO:area perdida
    arroz_perdida = (arroz_sembrada - arroz_cosechada)
    frijol_perdida = (frijol_sembrada - frijol_cosechada)
    maiz_perdida = (maiz_sembrada - maiz_cosechada)
    #TODO: produccion
    arroz_produccion = perdida.filter(primera__producto__id=1).aggregate(Sum('primera__produccion'))
    frijol_produccion = perdida.filter(primera__producto__id=2).aggregate(Sum('primera__produccion'))
    maiz_produccion = perdida.filter(primera__producto__id=3).aggregate(Sum('primera__produccion'))
    #TODO: rendimientos
    arroz_rendi = arroz_produccion / arroz_cosechada
    frijol_rendi = frijol_produccion / frijol_cosechada
    maiz_rendi = maiz_produccion / maiz_cosechada
    
    return render_to_response("encuesta/perdida.html",{'casos':casos,'arroz_sembrada':arroz_sembrada,
            'frijol_sembrada':frijol_sembrada,'maiz_sembrada':maiz_sembrada,
            'arroz_cosechada':arroz_cosechada,'frijol_cosechada':frijol_cosechada,
            'maiz_cosechada':maiz_cosechada,'arroz_perdida':arroz_perdida,'frijol_perdida':frijol_perdida,
            'maiz_perdida':maiz_perdida,'arroz_produccion':arroz_produccion,'frijol_produccion':frijol_produccion,
            'maiz_produccion':maiz_produccion,'arroz_rendi':arroz_rendi,
            'frijol_rendi':frijol_rendi,'maiz_rendi':maiz_rendi })
    
