# -*- encoding: utf-8 -*-

from django.db import models
from django.forms import ModelForm

from django import forms

# Create your models here.

##Creamos un modelo para los archivos de audio
class ficheros_audio(models.Model):

	nombre = models.CharField(max_length=80)

	descripcion = models.TextField(max_length=200)

	# En settings.py --> MEDIA_ROOT = '/home/asterisk-bee/asteriskbee'
	fichero_audio = models.FileField(upload_to='./api_admin_audio/sonidos')


#Creamos el formulario asociado a dicho modelo
class ficheroAudioForm(ModelForm):
	class Meta:
		model = ficheros_audio
		#exclude = ('commented','exten','app','appdata','priority')

