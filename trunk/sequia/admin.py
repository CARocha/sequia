from django.contrib import admin
from lugar.models import Comunidad
from sequia.models import Encuesta, Primera, Postrera, Apante, Disponibilidad, Nutricion, Organizacion, Entrevistado, Producto
from django.contrib.contenttypes import generic

class EntrevistadoInline(generic.GenericStackedInline):
    model = Entrevistado
    extra = 1
    max_num = 1
    
class PrimeraInline(generic.GenericTabularInline):
	model = Primera
	extra = 4
	max_num = 4

class PostreraInline(generic.GenericTabularInline):
	model = Postrera
	extra = 4
	max_num = 4

class ApanteInline(generic.GenericTabularInline):
	model = Apante
	extra = 4
	max_num = 4

class DisponibilidadInline(generic.GenericStackedInline):
	model = Disponibilidad
	extra = 1
	max_num = 1

class NutricionInline(generic.GenericTabularInline):
	model = Nutricion
	extra = 6
	max_num = 6
	
class EncuestaAdmin(admin.ModelAdmin):
	save_on_top = True
	actions_on_top = True
	inlines = [EntrevistadoInline,PrimeraInline,PostreraInline,ApanteInline,DisponibilidadInline,NutricionInline]
	list_display = []
	list_filter = ['fecha']
	date_hierarchy = 'fecha'
	search_fields = []

admin.site.register(Encuesta, EncuestaAdmin)
admin.site.register(Organizacion)
admin.site.register(Producto)