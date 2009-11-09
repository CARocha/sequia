 # -*- coding: UTF-8 -*-
 
from django.db import models
from lugar.models import Comunidad
import datetime
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

#Empieza las definiciones de las tablas de la base de datos
class Organizacion(models.Model):
    nombre = models.CharField('Nombre de la Organización', max_length=200, help_text="Introduzca el Nombre de la Organización")
    
    class Meta:
        verbose_name_plural="Organizacion"
        
    def __unicode__(self):
        return self.nombre
    
class Entrevistado(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField(db_index=True)
    content_object = generic.GenericForeignKey()
    nombre = models.CharField('Nombre del Entrevistado', max_length=200, help_text="Introduzca el nombre del entrevistado")
    comunidad = models.ForeignKey(Comunidad)
    
    class Meta:
        verbose_name_plural="Entrevistado"
        
    def __unicode__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField('Nombre del producto o cultivo', max_length=200, help_text="Introduzca el nombre del producto o cultivo")
    
    class Meta:
        verbose_name_plural = "Producto"
        
    def __unicode__(self):
        return self.nombre
class Perdida(models.Model):
    nombre = models.CharField('Nombre o Razón de pérdida', max_length=200, help_text="Introduzca la Razón de la perdida")
    
    class Meta:
        verbose_name_plural = "Razon de perdida"
    
    def __unicode__(self):
        return self.nombre
      
#PRODUCTO_CHOICES=((1,"Maíz"),(2,"Frijol"),(3,"Sorgo"))
#PERDIDA_CHOICES=((1,"Sequia"),(2,"Mala calidad de la semilla"),(3,"Ataque de plagas"))
class Primera(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField(db_index=True)
    content_object = generic.GenericForeignKey()
#    producto = models.IntegerField(choices=PRODUCTO_CHOICES)
    producto = models.ForeignKey(Producto)
    area_sembrada = models.DecimalField('Area sembrada en MZ', max_digits=10, decimal_places=2, help_text="Introduzca el area sembrada en Manzana")
    area_cosechada = models.DecimalField('Area cosechada en MZ', max_digits=10, decimal_places=2, help_text="Introduzca el area sembrada en Manzana")
    produccion = models.DecimalField('Producción en QQ', max_digits=10, decimal_places=2, help_text="Introduzca la producción en Quintales")
#    perdida = models.IntegerField(choices=PERDIDA_CHOICES)
    perdida = models.ForeignKey(Perdida)
    
    class Meta:
        verbose_name_plural="Sobre siembre de Primera"
        
    def __unicode__(self):
        return self.get_producto_display()
    
class Postrera(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField(db_index=True)
    content_object = generic.GenericForeignKey()
#    producto = models.IntegerField(choices=PRODUCTO_CHOICES)
    producto = models.ForeignKey(Producto)
    area_sembrada = models.DecimalField('Area sembrada en MZ', max_digits=10, decimal_places=2, help_text="Introduzca el area sembrada en Manzana")
    area_cosechada = models.DecimalField('Area cosechada en MZ', max_digits=10, decimal_places=2, help_text="Introduzca el area sembrada en Manzana")
    produccion = models.DecimalField('Producción en QQ', max_digits=10, decimal_places=2, help_text="Introduzca la producción en Quintales")
#    perdida = models.IntegerField(choices=PERDIDA_CHOICES)
    perdida = models.ForeignKey(Perdida)
    
    class Meta:
        verbose_name_plural="Sobre siembre de Postrera"
        
    def __unicode__(self):
        return self.get_producto_display()
    
class Apante(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField(db_index=True)
    content_object = generic.GenericForeignKey()
#    producto = models.IntegerField(choices=PRODUCTO_CHOICES)
    producto = models.ForeignKey(Producto)
    area_sembrada = models.DecimalField('Area sembrada en MZ', max_digits=10, decimal_places=2, help_text="Introduzca el area sembrada en Manzana")
    area_cosechada = models.DecimalField('Area cosechada en MZ', max_digits=10, decimal_places=2, help_text="Introduzca el area sembrada en Manzana")
    produccion = models.DecimalField('Producción en QQ', max_digits=10, decimal_places=2, help_text="Introduzca la producción en Quintales")
#    perdida = models.IntegerField(choices=PERDIDA_CHOICES)
    perdida = models.ForeignKey(Perdida)
    
    class Meta:
        verbose_name_plural="Sobre siembre de Apante"
        
    def __unicode__(self):
        return self.get_producto_display()
    
class Disponibilidad(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField(db_index=True)
    content_object = generic.GenericForeignKey()
    adultos_casa = models.IntegerField('Número de adultos que viven en la casa', help_text="Introduzca el número exacto de adultos")
    ninos_casa = models.IntegerField('Número de niños y niñas que viven en la casa', help_text="Introduzca el número exacto de niños y niñas")
    vacas = models.IntegerField(help_text="Número de vacas")
    cerdos = models.IntegerField(help_text="Número de cerdos")
    gallinas = models.IntegerField(help_text="Número de gallinas")
    maiz_disponible= models.DecimalField('QQ de Maíz disponible', max_digits=10, decimal_places=2, help_text="Cantidad de maíz disponible en la casa en quintales")
    frijol_disponible = models.DecimalField('QQ de Frijol disponible', max_digits=10, decimal_places=2, help_text="Cantidad de frijol disponible en la casa en quintales")
    sorgo_disponible = models.DecimalField('QQ de Sorgo disponible', max_digits=10, decimal_places=2, help_text="Cantidad de sorgo disponible en la casa en quintales")
    dinero = models.DecimalField('Cuanto Dinero', max_digits=10, decimal_places=2, help_text="Si tiene dinero guardado para comprar comida")
    
    class Meta:
        verbose_name_plural = "Sobre la disponibilidad de alimento"
    
class Nutricion(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField(db_index=True)
    content_object = generic.GenericForeignKey()
    ninos = models.CharField(max_length=50)
    edad = models.IntegerField()
    brazalete = models.CharField(max_length=200)
    
    class Meta:
        verbose_name_plural="Sobre estado de nutrición de los niños y niñas"
        
    def __unicode__(self):
        return self.brazalete
    
class Encuesta(models.Model):
    fecha = models.DateField()
    colector = models.CharField(max_length=100)
    organizacion = models.ForeignKey(Organizacion)
    entrevistado = generic.GenericRelation(Entrevistado)
    primera = generic.GenericRelation(Primera)
    postrera = generic.GenericRelation(Postrera)
    apante = generic.GenericRelation(Apante)
    disponibilidad = generic.GenericRelation(Disponibilidad)
    nutricion = generic.GenericRelation(Nutricion)
    
    def entrevista(self):
        return self.entrevistado.all()[0].nombre
