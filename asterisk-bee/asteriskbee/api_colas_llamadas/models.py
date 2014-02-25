# -*- encoding: utf-8 -*-

from django.db import models
from django.forms import ModelForm

from django import forms

# Modelo de COLAS DE LLAMADAS.

class colas(models.Model):

#	name VARCHAR(128) PRIMARY KEY,
	name = models.CharField(max_length=128,primary_key=True,verbose_name='Nombre')
#	musiconhold VARCHAR(128),
 	musiconhold = models.CharField(max_length=128,null=True,blank=True)
#	announce VARCHAR(128),
	announce = models.CharField(max_length=128,null=True,blank=True)
#	context VARCHAR(128),
	context = models.CharField(max_length=128,null=True,blank=True)
#	timeout INT(11),
	timeout = models.IntegerField(default=0,null=True,blank=True)
#	monitor_join tinyint(1),
	monitor_join =  models.IntegerField(default=0,null=True,blank=True)
#	monitor_format VARCHAR(128),
	monitor_format = models.CharField(max_length=128,null=True,blank=True)
#	queue_youarenext VARCHAR(128),
	queue_youarenext = models.CharField(max_length=128,null=True,blank=True)
#	queue_thereare VARCHAR(128),
	queue_thereare = models.CharField(max_length=128,null=True,blank=True)
#	queue_callswaiting VARCHAR(128),
	queue_callswaiting = models.CharField(max_length=128,null=True,blank=True)
#	queue_holdtime VARCHAR(128),
	queue_holdtime = models.CharField(max_length=128,null=True,blank=True)
#	queue_minutes VARCHAR(128),
	queue_minutes = models.CharField(max_length=128,null=True,blank=True)
#	queue_seconds VARCHAR(128),
	queue_seconds = models.CharField(max_length=128,null=True,blank=True)
#	queue_lessthan VARCHAR(128),
	queue_lessthan = models.CharField(max_length=128,null=True,blank=True)
#	queue_thankyou VARCHAR(128),
	queue_thankyou = models.CharField(max_length=128,null=True,blank=True)
#	queue_reporthold VARCHAR(128),
	queue_reporthold = models.CharField(max_length=128,null=True,blank=True)
#	announce_frequency INT(11),
	announce_frequency = models.IntegerField(default=0,null=True,blank=True)
#	announce_round_seconds INT(11),
	announce_round_seconds = models.IntegerField(default=0,null=True,blank=True)
#	announce_holdtime VARCHAR(128),
	announce_holdtime = models.CharField(max_length=128,null=True,blank=True)
#	retry INT(11),
	retry= models.IntegerField(default=0,null=True,blank=True)
#	wrapuptime INT(11),
	wrapuptime = models.IntegerField(default=0,null=True,blank=True)
#	maxlen INT(11),
	maxlen = models.IntegerField(default=0,null=True,blank=True)
#	servicelevel INT(11),
	servicelevel = models.IntegerField(default=0,null=True,blank=True)

#	strategy VARCHAR(128),
##    INFO del ficheor de configuracion /etc/asterisk/queues.conf
#   A strategy may be specified.  Valid strategies include:

# ringall - ring all available channels until one answers (default)
# leastrecent - ring interface which was least recently hung up by this queue
# fewestcalls - ring the one with fewest completed calls from this queue
# random - ring random interface
# rrmemory - round robin with memory, remember where we left off last ring pass
# rrordered - same as rrmemory, except the queue member order from config file 
#             is preserved
# linear - rings interfaces in the order specified in this configuration file.
#          If you use dynamic members, the members will be rung in the order in
#          which they were added
# wrandom - rings random interface, but uses the member's penalty as a weight
#           when calculating their metric. So a member with penalty 0 will have
#           a metric somewhere between 0 and 1000, and a member with penalty 1 will
#                       have a metric between 0 and 2000, and a member with penalty 2 will have
#           a metric between 0 and 3000. Please note, if using this strategy, the member
#           penalty is not the same as when using other queue strategies. It is ONLY used
#           as a weight for calculating metric.

	STRATEGY_CHOICES =(
                           ('ringall','ringall'),
                           ('leastrecent','leastrecent'),
                           ('fewestcalls','fewestcalls'),
                           ('random','random'),
                           ('rrmemory','rrmemory'),
                           ('rrordered','rrordered'),
                           ('linear','linear'),
                           ('wrandom','wrandom'),                           
                          )
      #  mode = models.CharField(max_length=6,choices=MODE_CHOICES,default='custom')
	strategy = models.CharField(max_length=128, choices=STRATEGY_CHOICES, default='ringall')

#	joinempty VARCHAR(128),
	joinempty = models.CharField(max_length=128,null=True,blank=True)
#	leavewhenempty VARCHAR(128),
	leavewhenempty = models.CharField(max_length=128,null=True,blank=True)
#	eventmemberstatus tinyint(1),
	eventmemberstatus = models.IntegerField(default=0,null=True,blank=True)
#	eventwhencalled tinyint(1),
	eventwhencalled = models.IntegerField(default=0,null=True,blank=True)
#	reportholdtime tinyint(1),
	reportholdtime = models.IntegerField(default=0,null=True,blank=True)
#	memberdelay INT(11),
	memberdelay = models.IntegerField(default=0,null=True,blank=True)
#	weight INT(11),
	weight = models.IntegerField(default=0,null=True,blank=True)
#	timeoutrestart tinyint(1),
	timeoutrestart = models.IntegerField(default=0,null=True,blank=True)
#	ringinuse tinyint(1),
	ringinuse = models.IntegerField(default=0,null=True,blank=True)
#	setinterfacevar tinyint(1));
	setinterfacevar = models.IntegerField(default=0,null=True,blank=True)


	def __str__(self):
		return '%s' % (self.name)




class miembros(models.Model):
 ##Para este modelohemos creado antes la tabla en la base de datos
#	CREATE TABLE api_colas_llamadas_miembros (
#	id INTEGER ,
#	membername VARCHAR(80),
#	queue_name VARCHAR(128),
#	interface VARCHAR(128),
#	penalty INTEGER,
#       paused INTEGER,
#       PRIMARY KEY (id)
#	);
#CREATE INDEX api_colas_llamadas_miembros__idx__queue_name_interface ON api_colas_llamadas_miembros(queue_name, interface);
	membername = models.CharField(max_length=80,null=True,blank=True)
	queue_name = models.CharField(max_length=128,null=True,blank=True)
	interface = models.CharField(max_length=128,null=True,blank=True)	
	penalty = models.IntegerField(null=True,blank=True)
	paused = models.IntegerField(null=True,blank=True)
	

	def __str__(self):
		return '%s -- %s' % (self.queue_name,self.interface)




#Creamos el formulario asociado a al modelo de cola de llamadas
class ColaLlamadaForm(ModelForm):
        class Meta:
                model = colas
                #exclude = ('format','sort','digit','mode','application','directory','nombre_mp3')


#Creamos el formulario asociado a al modelos de los miembros de la cola de llamadas
class MiembroColaLlamadasForm(ModelForm):
        class Meta:
                model = miembros
                #exclude = ('format','sort','digit','mode','application','directory','nombre_mp3')





