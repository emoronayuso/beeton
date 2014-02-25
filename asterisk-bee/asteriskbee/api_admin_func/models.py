# -*- encoding: utf-8 -*-

from django.db import models
from django.forms import ModelForm

from django import forms

# MODELO de la aplicacion de musica en espera

##Creamos un modelo para los archivos de audio
class func(models.Model):

	# En settings.py --> MEDIA_ROOT = '/home/asterisk-bee/asteriskbee'
	fichero_tar_gz = models.FileField(upload_to='./api_admin_func/pkg_instalados',verbose_name='Añadir funcionalidad')


#Creamos el formulario asociado a dicho modelo
class funcForm(ModelForm):
	class Meta:
		model = func

