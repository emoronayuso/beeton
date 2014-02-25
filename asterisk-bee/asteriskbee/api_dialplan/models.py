# -*- encoding: utf-8 -*-

from django.db import models
from django.forms import ModelForm

from django import forms

#encoding:utf-8

# Create your models here.


##Definimos una tabla que contendrá la información referente a la linea de un contexto
##Esta tabla es necesarioa para que Asterisk Realtime gestione el dialplan
class linea(models.Model):

#Definicion de campos 

##############################################################################################################
######NOTA MUY IMPORTANTE--->> NO CAMBIAR LA ESTRUCTURA DE LA TABLA si no Asterisk Realtime no funciona bien##
##############################################################################################################
##############################################################################################

        #Tabla SQLITE sacada de la guia oficial de DIGIUM para ASterisk 1.8
        #https://wiki.asterisk.org/wiki/download/attachments/19005471/Asterisk-Admin-Guide.pdf?api=v2
        #En la pagina 544, con dos atributos anadidos, nombre y apellidos, necesarios para el callerid. 
        #Por lo que crearemos un modelo de datos acorde con la estructura de dicha tabla:


#       CREATE TABLE api_dialplan_linea ( 
#           id INTEGER, 
#           commented TINYINT(1) NOT NULL DEFAULT 0, 
#           context VARCHAR(80) NOT NULL DEFAULT '', 
#           exten VARCHAR(40) NOT NULL DEFAULT '', 
#           priority INT(11) NOT NULL DEFAULT 0, 
#           app VARCHAR(128) NOT NULL DEFAULT '', 
#           appdata VARCHAR(128) NOT NULL DEFAULT '', 
#           PRIMARY KEY (id) 
#       );

#       CREATE INDEX api_dialplan_linea__idx__commented ON api_dialplan_linea(commented); 
#       CREATE INDEX api_dialplan_linea__idx__context_exten_priority ON api_dialplan_linea(context, exten, priority);
################################################################################################

#       commented TINYINT(1) NOT NULL DEFAULT 0,

	COMMENTED_CHOICES = (
                             ('1','si'),
                             ('0','no'),
                            )
	commented = models.CharField(max_length=1,choices=COMMENTED_CHOICES,default='0')

#       context VARCHAR(80) NOT NULL DEFAULT '',
	context = models.CharField(max_length=80,blank=True)

#	context = models.ForeignKey('contextos', db_column='context')

#       exten VARCHAR(40) NOT NULL DEFAULT '',
	exten = models.CharField(max_length=40,blank=True)

#       priority INT(11) NOT NULL DEFAULT 0,
	priority = models.IntegerField(default=0,blank=True)

#       app VARCHAR(128) NOT NULL DEFAULT '',
	app = models.CharField(max_length=128,blank=True,default='AGI')

#       appdata VARCHAR(128) NOT NULL DEFAULT '',
	appdata = models.CharField(max_length=128,blank=True)

	##Id de la linea
#	id = models.IntegerField(primary_key=True)

	def __str__(self):
		#return "CONTEXTO -> " + self.context.__str__() + "- exten => " + self.exten + "," + self.priority + "," + self.app + "(" + self.appdata + ")"

		return 'CONTEXTO -> %s - exten => %s,%s,%s(%s)' % (self.context, self.exten, self.priority, self.app, self.appdata)		


##Creamos una tabla de contextos
class contextos(models.Model):

	##Este atributo tipo Integer autoincrementado, es creado automaticamente en cada tabla por SQLite
	RowId = models.IntegerField()

        nombre = models.CharField(max_length=80, primary_key=True)
	

	def __str__(self):
		return self.nombre

##Modelo Aplicaciones para la gestion de funcionalidades del dialplan
class aplicaciones(models.Model):

	####Nombre de la aplicacion############
	nombre = models.CharField(max_length=80,blank=True)

	###Descripcion de la aplicacion##############
	descripcion = models.TextField(max_length=300,blank=True)

	##nombre del script python##############	
	script = models.CharField(max_length=80,blank=True)

	###Numero de parametros necesarios######
	num_para = models.IntegerField(default=0,blank=True)

	##color asignado######################
	###Formato: '#FF0000' ################
	color = models.CharField(max_length=9,blank=True) 

	###Nombre del archivo html de la plantilla##### Guardado en templates/dialplan/temp_api_instaladas/ ##
	nom_arch_temp = models.CharField(max_length=80,blank=True)

	##############Nombre de cada uno de los parametros de la aplicacion y sus textos de ayuda########
	################################################################################################
	#####Nombre,descripcion y bit de activacion de template del Parametro 1######
	nom_param1 = models.CharField(max_length=80,blank=True)
	des_param1 = models.CharField(max_length=200,blank=True)
	temp_param1 = models.CharField(max_length=1,default='0')

	#####Nombre,descripcion y bit de activacion de template del Parametro 2######
	nom_param2 = models.CharField(max_length=80,blank=True)
	des_param2 = models.CharField(max_length=200,blank=True)
	temp_param2 = models.CharField(max_length=1,default='0')

	#####Nombre,descripcion y bit de activacion de template del Parametro 3######
	nom_param3 = models.CharField(max_length=80,blank=True)
	des_param3 = models.CharField(max_length=200,blank=True)
	temp_param3 = models.CharField(max_length=1,default='0')

	#####Nombre,descripcion y bit de activacion de template del Parametro 4######
	nom_param4 = models.CharField(max_length=80,blank=True)
	des_param4 = models.CharField(max_length=200,blank=True)
	temp_param4 = models.CharField(max_length=1,default='0')	

	#####Nombre,descripcion y bit de activacion de template del Parametro 5######
	nom_param5 = models.CharField(max_length=80,blank=True)
	des_param5 = models.CharField(max_length=200,blank=True)
	temp_param5 = models.CharField(max_length=1,default='0')

	#####Nombre,descripcion y bit de activacion de template del Parametro 6######
	nom_param6 = models.CharField(max_length=80,blank=True)
	des_param6 = models.CharField(max_length=200,blank=True)
	temp_param6 = models.CharField(max_length=1,default='0')

	#####Nombre,descripcion y bit de activacion de template del Parametro 7######
	nom_param7 = models.CharField(max_length=80,blank=True)
	des_param7 = models.CharField(max_length=200,blank=True)
	temp_param7 = models.CharField(max_length=1,default='0')

	#####Nombre,descripcion y bit de activacion de template del Parametro 8######
	nom_param8 = models.CharField(max_length=80,blank=True)
	des_param8 = models.CharField(max_length=200,blank=True)
	temp_param8 = models.CharField(max_length=1,default='0')

	#####Nombre,descripcion y bit de activacion de template del Parametro 9######
	nom_param9 = models.CharField(max_length=80,blank=True)
	des_param9 = models.CharField(max_length=200,blank=True)
	temp_param9 = models.CharField(max_length=1,default='0')

	#####Nombre,descripcion y bit de activacion de template del Parametro 10######
	nom_param10 = models.CharField(max_length=80,blank=True)
	des_param10 = models.CharField(max_length=200,blank=True)
	temp_param10 = models.CharField(max_length=1,default='0')
	
	def __str__(self):
		return 'API -> %s, con %s parametros - script => %s' % (self.nombre, self.num_para, self.script)


##Modelo parametros para la gestion de los parametros de las funcionalidades del dialplan
class parametros(models.Model):

	#Relacion con la tabla linea
        id_linea = models.ForeignKey('linea', db_column='id_linea')

	#Relacion con la tabla aplicaciones
	id_api = models.ForeignKey('aplicaciones', db_column='id_api')
	

	###10 parametros
	param1 = models.CharField(max_length=200,blank=True)

	param2 = models.CharField(max_length=200,blank=True)

	param3 = models.CharField(max_length=200,blank=True)

	param4 = models.CharField(max_length=200,blank=True)

	param5 = models.CharField(max_length=200,blank=True)

	param6 = models.CharField(max_length=200,blank=True)

	param7 = models.CharField(max_length=200,blank=True)

	param8 = models.CharField(max_length=200,blank=True)

	param9 = models.CharField(max_length=200,blank=True)

	param10 = models.CharField(max_length=200,blank=True)




####### FORMULARIOS A PARTIR DE MODELOS ##################
## Creamos el formulario a partir del modelo linea para mostrar solo el nombre del contexto
class contextoForm(ModelForm):
        class Meta:
                model = linea
		exclude = ('commented','exten','app','appdata','priority')

##Creamos el formulario a partir del modelo linea
class lineaContextoForm(ModelForm):
        class Meta:
		model = linea
		#exclude = ('commented', 'context','app','appdata','priority')
		#Ponemos algunos atributos de la linea ocultos
		commented = forms.CharField(widget=forms.HiddenInput)
		context = forms.CharField(widget=forms.HiddenInput)
		app = forms.CharField(widget=forms.HiddenInput)
		appdata = forms.CharField(widget=forms.HiddenInput)	
		priority = forms.CharField(widget=forms.HiddenInput)
		widgets = {
                           'commented' : forms.HiddenInput(),
                           'context' : forms.HiddenInput(),
                           'app' : forms.HiddenInput(),
                           'appdata' : forms.HiddenInput(),
                           'priority' : forms.HiddenInput(),
                          }



##########################################FORMULARIOS PARA MOSTRAR LA APLICACION###############################
##Creamos el formulario a partir del modelo aplicaciones
class aplicacionContextoForm(ModelForm):
	class Meta:
		model = aplicaciones
		#fields = ('name', 'birth_date')
		exclude = ('num_para','color')
		###Ponemos el atributo script oculto en el formulario porque hace falta para crear una nueva linea
		##Y el atributo id para crear la nueva tupla de parametros
		script = forms.CharField(widget=forms.HiddenInput)
		id     = forms.IntegerField(widget=forms.HiddenInput)
		widgets = {
                            'script' : forms.HiddenInput(),
                            'id' : forms.HiddenInput(),
                          }


##Formulario de la aplicacion que solo muestra el nombre de los parametros
class aplicacionContextoParamForm(ModelForm):
	class Meta:
		model = aplicaciones
		fields = ('nom_param1','nom_param2','nom_param3','nom_param4','nom_param5','nom_param6','nom_param7','nom_param8','nom_param9','nom_param10')

		nom_param1 = forms.CharField(widget= forms.TextInput)
		nom_param2 = forms.CharField(widget= forms.TextInput)
		nom_param3 = forms.CharField(widget= forms.TextInput)
		nom_param4 = forms.CharField(widget= forms.TextInput)
		nom_param5 = forms.CharField(widget= forms.TextInput)
		nom_param6 = forms.CharField(widget= forms.TextInput)
		nom_param7 = forms.CharField(widget= forms.TextInput)
		nom_param8 = forms.CharField(widget= forms.TextInput)
		nom_param9 = forms.CharField(widget= forms.TextInput)
		nom_param10 = forms.CharField(widget= forms.TextInput)



		widgets = {
                            'nom_param1' : forms.TextInput(attrs={'readonly': 'readonly'}),
                            'nom_param2' : forms.TextInput(attrs={'readonly': 'readonly'}),
                            'nom_param3' : forms.TextInput(attrs={'readonly': 'readonly'}),
                            'nom_param4' : forms.TextInput(attrs={'readonly': 'readonly'}),
                            'nom_param5' : forms.TextInput(attrs={'readonly': 'readonly'}),
                            'nom_param6' : forms.TextInput(attrs={'readonly': 'readonly'}),
                            'nom_param7' : forms.TextInput(attrs={'readonly': 'readonly'}),
                            'nom_param8' : forms.TextInput(attrs={'readonly': 'readonly'}),
                            'nom_param9' : forms.TextInput(attrs={'readonly': 'readonly'}),
                            'nom_param10' : forms.TextInput(attrs={'readonly': 'readonly'}),
                          }




##Formulario de la aplicacion que solo muestra la descripcion de cada uno de los parametros
class aplicacionContextoDesParamForm(ModelForm):
	class Meta:
		model = aplicaciones
		fields = ('des_param1','des_param2','des_param3','des_param4','des_param5','des_param6','des_param7','des_param8','des_param9','des_param10')

		des_param1 = forms.CharField(widget= forms.TextInput)
		des_param2 = forms.CharField(widget= forms.TextInput)
		des_param3 = forms.CharField(widget= forms.TextInput)
		des_param4 = forms.CharField(widget= forms.TextInput)
		des_param5 = forms.CharField(widget= forms.TextInput)
		des_param6 = forms.CharField(widget= forms.TextInput)
		des_param7 = forms.CharField(widget= forms.TextInput)
		des_param8 = forms.CharField(widget= forms.TextInput)
		des_param9 = forms.CharField(widget= forms.TextInput)
		des_param10 = forms.CharField(widget= forms.TextInput)
		


		widgets = {
                            'des_param1' : forms.TextInput(attrs={'readonly': 'readonly'}),
                            'des_param2' : forms.TextInput(attrs={'readonly': 'readonly'}),
                            'des_param3' : forms.TextInput(attrs={'readonly': 'readonly'}),
                            'des_param4' : forms.TextInput(attrs={'readonly': 'readonly'}),
                            'des_param5' : forms.TextInput(attrs={'readonly': 'readonly'}),
                            'des_param6' : forms.TextInput(attrs={'readonly': 'readonly'}),
                            'des_param7' : forms.TextInput(attrs={'readonly': 'readonly'}),
                            'des_param8' : forms.TextInput(attrs={'readonly': 'readonly'}),
                            'des_param9' : forms.TextInput(attrs={'readonly': 'readonly'}),
                            'des_param10' : forms.TextInput(attrs={'readonly': 'readonly'}),
		          }



##Formulario que solo muestra el bit de activacion de la plantilla del formulario del parametro
class aplicacionBitActTemplateParamForm(ModelForm):
	class Meta:
		model = aplicaciones
		fields = ('temp_param1','temp_param2','temp_param3','temp_param4','temp_param5','temp_param6','temp_param7','temp_param8','temp_param9','temp_param10')
#################################################################################################################


#Creamos un formulario para mostrar los parametros de la linea a partir del modelo parametros
class parametrosLineaContextoForm(ModelForm):
	class Meta:
		model = parametros
		exclude = ('id_api','id_linea')
