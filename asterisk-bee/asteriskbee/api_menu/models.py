from django.db import models

# Create your models here.

class Categoria(models.Model):
	#Definicion de campo
	slug = models.SlugField(blank=False,unique=True)
	nombre = models.CharField(max_length=250,unique=True)
	posicion = models.IntegerField() 	
	icono = models.CharField(max_length=50)	

	def get_absolute_url(self):
		return "/admin/%s/" % self.slug
	def __unicode__(self):
		return u'%s' % self.nombre

	#Funcion string que muestra el nombre junto con la posicion
	def __str__(self):
		return '%s - %s' % (self.posicion,self.nombre)
	
	# A menos que se proporcione un ordenamiento mediante ordering,
	# se ordenaran los modelos de Categoria por su atributo posicion
	class Meta:
		ordering = ["posicion"]
