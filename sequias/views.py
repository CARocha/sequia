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
from pygooglechart import PieChart3D, StackedVerticalBarChart

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
    return direct_to_template(request, 'index.html', dict)

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
@session_required
def perdidapostrera(request):
    fecha1=request.session['fecha_inicio']
    fecha2=request.session['fecha_final']
    if request.session['comunidad']:
        com = request.session['comunidad'].id
        if request.session['entrevistado'] !=None:
            perdida = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__nombre=request.session['entrevistado'])
        else:
            perdida = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__comunidad__id=com)
    elif request.session['municipio']:
        mun = request.session['municipio'].id
        if request.session['entrevistado'] !=None:
            perdida = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__nombre=request.session['entrevistado'])
        else:
            perdida = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__comunidad__municipio__id=mun)
    elif request.session['departamento']:
        dep = request.session['departamento'].id
        if request.session['entrevistado'] !=None:
            perdida = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__nombre=request.session['entrevistado'])
        else:
            perdida = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__comunidad__municipio__departamento__id=dep)
    elif request.session['entrevistado']:
        entre = request.session['entrevistado']
        perdida = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__nombre=entre)
    else:
        perdida = Encuesta.objects.all()
        
    casos = perdida.count()
    #TODO: Sumatorias de maiz,frijol,sorgo CICLO PRIMERA
    arroz_sembrada = perdida.filter(primera__producto__id=4).aggregate(Sum('primera__area_sembrada'))['primera__area_sembrada__sum']
    frijol_sembrada = perdida.filter(primera__producto__id=3).aggregate(Sum('primera__area_sembrada'))['primera__area_sembrada__sum']
    maiz_sembrada = perdida.filter(primera__producto__id=2).aggregate(Sum('primera__area_sembrada'))['primera__area_sembrada__sum']
    #TODO: area cosechada
    arroz_cosechada = perdida.filter(primera__producto__id=4).aggregate(Sum('primera__area_cosechada'))['primera__area_cosechada__sum']
    frijol_cosechada = perdida.filter(primera__producto__id=3).aggregate(Sum('primera__area_cosechada'))['primera__area_cosechada__sum']
    maiz_cosechada = perdida.filter(primera__producto__id=2).aggregate(Sum('primera__area_cosechada'))['primera__area_cosechada__sum']
    #TODO:area perdida
    try:
        arroz_perdida = (arroz_sembrada - arroz_cosechada)
    except:
        pass
    try:
        frijol_perdida = (frijol_sembrada - frijol_cosechada)
    except:
        pass
    try:
        maiz_perdida = (maiz_sembrada - maiz_cosechada)
    except:
        pass
    #TODO: produccion
    arroz_produccion = perdida.filter(primera__producto__id=4).aggregate(Sum('primera__produccion'))['primera__produccion__sum']
    frijol_produccion = perdida.filter(primera__producto__id=3).aggregate(Sum('primera__produccion'))['primera__produccion__sum']
    maiz_produccion = perdida.filter(primera__producto__id=2).aggregate(Sum('primera__produccion'))['primera__produccion__sum']
    #TODO: rendimientos
    try:
        arroz_rendi = arroz_produccion / arroz_cosechada
    except:
        pass
    try:
        frijol_rendi = frijol_produccion / frijol_cosechada
    except:
        pass
    try:
        maiz_rendi = maiz_produccion / maiz_cosechada
    except:
        pass
    
    #TODO: CICLO POSTRERA
    arroz_sembrada_P = perdida.filter(postrera__producto__id=4).aggregate(Sum('postrera__area_sembrada'))['postrera__area_sembrada__sum']
    frijol_sembrada_P = perdida.filter(postrera__producto__id=3).aggregate(Sum('postrera__area_sembrada'))['postrera__area_sembrada__sum']
    maiz_sembrada_P = perdida.filter(postrera__producto__id=2).aggregate(Sum('postrera__area_sembrada'))['postrera__area_sembrada__sum'] 
    #TODO: area cosechada
    arroz_cosechada_P = perdida.filter(postrera__producto__id=4).aggregate(Sum('postrera__area_cosechada'))['postrera__area_cosechada__sum']
    frijol_cosechada_P = perdida.filter(postrera__producto__id=3).aggregate(Sum('postrera__area_cosechada'))['postrera__area_cosechada__sum']
    maiz_cosechada_P = perdida.filter(postrera__producto__id=2).aggregate(Sum('postrera__area_cosechada'))['postrera__area_cosechada__sum']
    #TODO:area perdida
    try:
        arroz_perdida_P = arroz_sembrada_P - arroz_cosechada_P
    except:
        pass
    try:
        frijol_perdida_P = frijol_sembrada_P - frijol_cosechada_P
    except:
        pass
    try:
        maiz_perdida_P = maiz_sembrada_P - maiz_cosechada_P
    except:
        pass
    #TODO: produccion
    arroz_produccion_P = perdida.filter(postrera__producto__id=4).aggregate(Sum('postrera__produccion'))['postrera__produccion__sum']
    frijol_produccion_P = perdida.filter(postrera__producto__id=3).aggregate(Sum('postrera__produccion'))['postrera__produccion__sum']
    maiz_produccion_P = perdida.filter(postrera__producto__id=2).aggregate(Sum('postrera__produccion'))['postrera__produccion__sum']
    #TODO: rendimientos
    try:
        arroz_rendi_P = arroz_produccion_P / arroz_cosechada_P
    except:
        pass
    try:
        frijol_rendi_P = frijol_produccion_P / frijol_cosechada_P
    except:
        pass
    try:
        maiz_rendi_P = maiz_produccion_P / maiz_cosechada_P
    except:
        pass
    return render_to_response("encuesta/perdida.html", locals())

@session_required    
def disponibilidad(request):
    fecha1=request.session['fecha_inicio']
    fecha2=request.session['fecha_final']
    if request.session['comunidad']:
        com = request.session['comunidad'].id
        if request.session['entrevistado'] !=None:
            dispo = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__nombre=request.session['entrevistado'])
        else:
            dispo = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__comunidad__id=com)
    elif request.session['municipio']:
        mun = request.session['municipio'].id
        if request.session['entrevistado'] !=None:
            dispo = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__nombre=request.session['entrevistado'])
        else:
            dispo = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__comunidad__municipio__id=mun)
    elif request.session['departamento']:
        dep = request.session['departamento'].id
        if request.session['entrevistado'] !=None:
            dispo = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__nombre=request.session['entrevistado'])
        else:
            dispo = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__comunidad__municipio__departamento__id=dep)
    elif request.session['entrevistado']:
        entre = request.session['entrevistado'].id
        dispo = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__nombre=entre)
    else:
        dispo = Encuesta.objects.all()
        
    casos = dispo.count()
    #TODO: sumas de toda la tabla disponibilidad
    total_adulto= dispo.aggregate(Sum('disponibilidad__adultos_casa'))['disponibilidad__adultos_casa__sum']
    total_ninos=dispo.aggregate(Sum('disponibilidad__ninos_casa'))['disponibilidad__ninos_casa__sum']
    total_vacas = dispo.aggregate(Sum('disponibilidad__vacas'))['disponibilidad__vacas__sum']
    total_cerdos = dispo.aggregate(Sum('disponibilidad__cerdos'))['disponibilidad__cerdos__sum']
    total_gallinas =dispo.aggregate(Sum('disponibilidad__gallinas'))['disponibilidad__gallinas__sum']
    total_maiz=dispo.aggregate(Sum('disponibilidad__maiz_disponible'))['disponibilidad__maiz_disponible__sum']
    total_frijol=dispo.aggregate(Sum('disponibilidad__frijol_disponible'))['disponibilidad__frijol_disponible__sum']
    total_sorgo=dispo.aggregate(Sum('disponibilidad__sorgo_disponible'))['disponibilidad__sorgo_disponible__sum']
    prom_maiz=total_maiz/casos
    prom_frijol=total_frijol/casos
    prom_sorgo=total_sorgo/casos
    try:
        criterio1 = (float(total_maiz) * 100) / ((float(total_adulto) * 1) + (float(total_ninos) * 0.9))
    except:
        pass
    try:
        criterio2 = (float(total_frijol) * 100) / ((float(total_adulto) * 0.5) + (float(total_ninos) * 0.4))
    except:
        pass
    try:
        criterio3 = ((float(total_maiz) + float(total_sorgo)) * 100) / ((float(total_adulto) * 1) + (float(total_ninos) * 0.9) + (total_cerdos * 2.5)+(total_gallinas * 0.156))
    except:
        pass
    
    return render_to_response("encuesta/disponibilidad.html", locals())

@session_required
def nutricion(request):
    fecha1=request.session['fecha_inicio']
    fecha2=request.session['fecha_final']
    if request.session['comunidad']:
        com = request.session['comunidad'].id
        if request.session['entrevistado'] !=None:
            nutri = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__nombre=request.session['entrevistado'])
        else:
            nutri = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__comunidad__id=com)
    elif request.session['municipio']:
        mun = request.session['municipio'].id
        if request.session['entrevistado'] !=None:
            nutri = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__nombre=request.session['entrevistado'])
        else:
            nutri = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__comunidad__municipio__id=mun)
    elif request.session['departamento']:
        dep = request.session['departamento'].id
        if request.session['entrevistado'] !=None:
            nutri = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__nombre=request.session['entrevistado'])
        else:
            nutri = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__comunidad__municipio__departamento__id=dep)
    elif request.session['entrevistado']:
        entre = request.session['entrevistado'].id
        nutri = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__nombre=entre)
    else:
        nutri = Encuesta.objects.all()
        
    casos = nutri.count()
    #TODO: hacer sumas otra ves :P, rango 1 - 5  niños
    ninos_normal = nutri.filter(nutricion__edad__range=(1,5)).filter(nutricion__ninos__contains="ninos").filter(nutricion__brazalete__id=1).count()
    ninos_riesgo = nutri.filter(nutricion__edad__range=(1,5)).filter(nutricion__ninos__contains="ninos").filter(nutricion__brazalete__id=4).count()
    ninos_desnutrido = nutri.filter(nutricion__edad__range=(1,5)).filter(nutricion__ninos__contains="ninos").filter(nutricion__brazalete__id=3).count()
    ninos_nosabe = nutri.filter(nutricion__edad__range=(1,5)).filter(nutricion__ninos__contains="ninos").filter(nutricion__brazalete__id=5).count()
    #TODO: rango 6 - 10 niños
    ninos_normal_s = nutri.filter(nutricion__edad__range=(6,10)).filter(nutricion__ninos__contains="ninos").filter(nutricion__brazalete__id=1).count()
    ninos_riesgo_s = nutri.filter(nutricion__edad__range=(6,10)).filter(nutricion__ninos__contains="ninos").filter(nutricion__brazalete__id=4).count()
    ninos_desnutrido_s = nutri.filter(nutricion__edad__range=(6,10)).filter(nutricion__ninos__contains="ninos").filter(nutricion__brazalete__id=3).count()
    ninos_nosabe_s = nutri.filter(nutricion__edad__range=(6,10)).filter(nutricion__ninos__contains="ninos").filter(nutricion__brazalete__id=5).count()
    #TODO: rango 11 - 15 niños
    ninos_normal_o = nutri.filter(nutricion__edad__range=(11,15)).filter(nutricion__ninos__contains="ninos").filter(nutricion__brazalete__id=1).count()
    ninos_riesgo_o = nutri.filter(nutricion__edad__range=(11,15)).filter(nutricion__ninos__contains="ninos").filter(nutricion__brazalete__id=4).count()
    ninos_desnutrido_o = nutri.filter(nutricion__edad__range=(11,15)).filter(nutricion__ninos__contains="ninos").filter(nutricion__brazalete__id=3).count()
    ninos_nosabe_o = nutri.filter(nutricion__edad__range=(11,15)).filter(nutricion__ninos__contains="ninos").filter(nutricion__brazalete__id=5).count()
    #TODO: NIÑAS 1-5
    ninas_normal = nutri.filter(nutricion__edad__range=(1,5)).filter(nutricion__ninos__contains="ninas").filter(nutricion__brazalete__id=1).count()
    ninas_riesgo = nutri.filter(nutricion__edad__range=(1,5)).filter(nutricion__ninos__contains="ninas").filter(nutricion__brazalete__id=4).count()
    ninas_desnutrido = nutri.filter(nutricion__edad__range=(1,5)).filter(nutricion__ninos__contains="ninas").filter(nutricion__brazalete__id=3).count()
    ninas_nosabe = nutri.filter(nutricion__edad__range=(1,5)).filter(nutricion__ninos__contains="ninas").filter(nutricion__brazalete__id=5).count()
    #TODO: rango 6 - 10 niñas
    ninas_normal_s = nutri.filter(nutricion__edad__range=(6,10)).filter(nutricion__ninos__contains="ninas").filter(nutricion__brazalete__id=1).count()
    ninas_riesgo_s = nutri.filter(nutricion__edad__range=(6,10)).filter(nutricion__ninos__contains="ninas").filter(nutricion__brazalete__id=4).count()
    ninas_desnutrido_s = nutri.filter(nutricion__edad__range=(6,10)).filter(nutricion__ninos__contains="ninas").filter(nutricion__brazalete__id=3).count()
    ninas_nosabe_s = nutri.filter(nutricion__edad__range=(6,10)).filter(nutricion__ninos__contains="ninas").filter(nutricion__brazalete__id=5).count()
    #TODO: rango 11 - 15 niñas
    ninas_normal_o = nutri.filter(nutricion__edad__range=(11,15)).filter(nutricion__ninos__contains="ninas").filter(nutricion__brazalete__id=1).count()
    ninas_riesgo_o = nutri.filter(nutricion__edad__range=(11,15)).filter(nutricion__ninos__contains="ninas").filter(nutricion__brazalete__id=4).count()
    ninas_desnutrido_o = nutri.filter(nutricion__edad__range=(11,15)).filter(nutricion__ninos__contains="ninas").filter(nutricion__brazalete__id=3).count()
    ninas_nosabe_o = nutri.filter(nutricion__edad__range=(11,15)).filter(nutricion__ninos__contains="ninas").filter(nutricion__brazalete__id=5).count()
    
    
    return render_to_response("encuesta/nutricion.html", locals())

def grafo_perdida(request):
    fecha1=request.session['fecha_inicio']
    fecha2=request.session['fecha_final']
    if request.session['comunidad']:
        com = request.session['comunidad'].id
        if request.session['entrevistado'] !=None:
            gperdida = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__nombre=request.session['entrevistado'])
        else:
            gperdida = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__comunidad__id=com)
    elif request.session['municipio']:
        mun = request.session['municipio'].id
        if request.session['entrevistado'] !=None:
            gperdida = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__nombre=request.session['entrevistado'])
        else:
            gperdida = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__comunidad__municipio__id=mun)
    elif request.session['departamento']:
        dep = request.session['departamento'].id
        if request.session['entrevistado'] !=None:
            gperdida = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__nombre=request.session['entrevistado'])
        else:
            gperdida = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__comunidad__municipio__departamento__id=dep)
    elif request.session['entrevistado']:
        entre = request.session['entrevistado']
        gperdida = Encuesta.objects.filter(fecha__range=(fecha1,fecha2)).filter(entrevistado__nombre=entre)
    else:
        gperdida = Encuesta.objects.all()
        
    casos = gperdida.count()
    maiz_s = 0
    maiz_c = 0
    for encuesta in gperdida:
     for primera in encuesta.primera.all():
        maiz_s = primera.area_sembrada + maiz_s
        maiz_c = primera.area_cosechada + maiz_c
		
    resta = maiz_s - maiz_c
    
    p_c = (float(maiz_c)) *100
    p_p = (float(resta)) *100

    graph = PieChart3D(400,200)
    graph.set_colours([ 'FFBC13','22A410',])
    graph.add_data([p_c,p_p])
    graph.set_legend(['area cosechada','area perdidad'])
#    porcentajes = saca_porcentajes([data[1] for data in resultados])
    graph.set_pie_labels(['p_c','p_p'])
    graph.set_legend_position("b")
    graph.set_title("Maiz")
    url = graph.get_url()
    print url
    
    return render_to_response("encuesta/grafos.html",{ 'url':url })
