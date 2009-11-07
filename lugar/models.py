from django.db import models

# Create your models here.
class Departamento(models.Model):
	nombre = models.CharField(max_length=40)

	class Meta:
		verbose_name_plural="Departamento"

	def __unicode__(self):
		return self.nombre

class Municipio(models.Model):
	departamento = models.ForeignKey(Departamento)
	nombre = models.CharField(max_length=40)
    
	class Meta:
		verbose_name_plural = "Municipio"
         
	def __unicode__(self):
		return self.nombre

class Microcuenca(models.Model):
	nombre = models.CharField(max_length=100)
	
	class Meta:
		verbose_name_plural="Microcuenca"

	def __unicode__(self):
		return self.nombre

class Comunidad(models.Model):
	municipio = models.ForeignKey(Municipio)
	microcuenca = models.ForeignKey(Microcuenca,null=True,blank=True)
	nombre = models.CharField(max_length=40)

	class Meta:
		verbose_name_plural="Comunidad"

	def __unicode__(self):
		return self.nombre

