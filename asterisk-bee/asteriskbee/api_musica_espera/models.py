# -*- encoding: utf-8 -*-

from django.db import models
from django.forms import ModelForm

from django import forms

# MODELO de la aplicacion de musica en espera

##Creamos un modelo para los archivos de audio
class moh(models.Model):

	#'name' varchar(80) NOT NULL, PRIMARY KEY ('name'));
	name = models.CharField(max_length=80,primary_key=True,verbose_name='Nombre')

	##Directorio donde estaran los ficeros de audio de la musica en espera,	
	#'directory' varchar(255) NOT NULL default ,
	directory = models.CharField(max_length=255,default='/home/asterisk-bee/asteriskbee/api_musica_espera/ficheros_audio')
	
	#'application' varchar(255) NOT NULL default ,
	application = models.CharField(max_length=255,null=True,blank=True)

	#'mode' varchar(80) NOT NULL default ,
	MODE_CHOICES =(
                       ('files','files'),
                       ('custom','custom'),
                       ('quietmp3','quietmp3'),
                      )
	mode = models.CharField(max_length=6,choices=MODE_CHOICES,default='custom')

	#Digito que podrá pulsar el usuario para dejar de escuchar la musica en espera, por defecto ponemos '#'
	#'digit' char(1) NOT NULL default ,
	digit = models.CharField(max_length=1,default='#')

	# Indica el orden de reproducion de los archivos (alpha, en orden alfabetivo. random aleatorio)
	#'sort' varchar(16) NOT NULL default ,
	sort =  models.CharField(max_length=16,null=True,blank=True)

	#Formato de fichero de audio (alaw,ulaw...)
	#'format' varchar(16) NOT NULL default ,
	format = models.CharField(max_length=16,null=True,blank=True)

	# En settings.py --> MEDIA_ROOT = '/home/asterisk-bee/asteriskbee'
	fichero_audio = models.FileField(upload_to='./api_musica_espera/ficheros_audio')

	nombre_mp3 =  models.CharField(max_length=255,null=True,blank=True)

	def __str__(self):

                return '%s' % (self.name)




#Creamos el formulario asociado a dicho modelo
class MohForm(ModelForm):
        class Meta:
                model = moh
                exclude = ('format','sort','digit','mode','application','directory','nombre_mp3')



