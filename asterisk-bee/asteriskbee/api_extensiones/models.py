from django.db import models
from django.forms import ModelForm

from django import forms

#Incluimos del modelo linea del dialplan para generar de forma dinamica el choices de context
from asteriskbee.api_dialplan.models import linea


#encoding:utf-8

# Create your models here.
#Creamos las clases correspondientes a los modelos de las extensiones SIP y IAX

class sip(models.Model): 
        #Definicion de campos 

##############################################################################################
	#Tabla SQLITE sacada de la guia oficial de DIGIUM para ASterisk 1.8
	#https://wiki.asterisk.org/wiki/download/attachments/19005471/Asterisk-Admin-Guide.pdf?api=v2
	#En la pagina 544, con dos atributos anadidos, nombre y apellidos, necesarios para el callerid. 
	#Por lo que crearemos un modelo de datos acorde con la estructura de dicha tabla:
	


#     CREATE TABLE api_extensiones_sip ( 
#	id INTEGER, 
#	commented TINYINT(1) NOT NULL DEFAULT 0,
#       nombre VARCHAR(80) NOT NULL DEFAULT '',
#       apellidos VARCHAR(80) NOT NULL DEFAULT '', 
#	name VARCHAR(80) NOT NULL DEFAULT '', 
#	host VARCHAR(31) NOT NULL DEFAULT '', 
#	nat VARCHAR(5) NOT NULL DEFAULT 'no', 
#	type VARCHAR(6) NOT NULL DEFAULT 'friend', 
#	accountcode VARCHAR(20) DEFAULT NULL, 
#	amaflags VARCHAR(13) DEFAULT NULL, 
#	callgroup VARCHAR(10) DEFAULT NULL, 
#	callerid VARCHAR(80) DEFAULT NULL, 
#	cancallforward CHAR(3) DEFAULT 'yes', 
#	directmedia CHAR(3) DEFAULT 'yes', 
#	context VARCHAR(80) DEFAULT NULL, 
#	defaultip VARCHAR(15) DEFAULT NULL, 
#	dtmfmode VARCHAR(7) DEFAULT NULL, 
#	fromuser VARCHAR(80) DEFAULT NULL, 
#	fromdomain VARCHAR(80) DEFAULT NULL, 
#	insecure VARCHAR(4) DEFAULT NULL, 
#	language CHAR(2) DEFAULT NULL, 
#	mailbox VARCHAR(50) DEFAULT NULL, 
#	md5secret VARCHAR(80) DEFAULT NULL, 
#	deny VARCHAR(95) DEFAULT NULL, 
#	permit VARCHAR(95) DEFAULT NULL, 
#	mask VARCHAR(95) DEFAULT NULL,
#	musiconhold VARCHAR(100) DEFAULT NULL, 
#	pickupgroup VARCHAR(10) DEFAULT NULL, 
#	qualify CHAR(3) DEFAULT NULL, 
#	regexten VARCHAR(80) DEFAULT NULL, 
#	restrictcid CHAR(3) DEFAULT NULL, 
#	rtptimeout CHAR(3) DEFAULT NULL, 
#	rtpholdtimeout CHAR(3) DEFAULT NULL, 
#	secret VARCHAR(80) DEFAULT NULL, 
#	setvar VARCHAR(100) DEFAULT NULL, 
#	disallow VARCHAR(100) DEFAULT 'all', 
#	allow VARCHAR(100) DEFAULT 'g729,ilbc,gsm,ulaw,alaw', 
#	fullcontact VARCHAR(80) NOT NULL DEFAULT '', 
#	ipaddr VARCHAR(15) NOT NULL DEFAULT '', 
#	port INT(11) NOT NULL DEFAULT 0, 
#	regserver VARCHAR(100) DEFAULT NULL, 
#	regseconds INT(11) NOT NULL DEFAULT 0, 
#	username VARCHAR(80) NOT NULL DEFAULT '', 
#	PRIMARY KEY (id) 
#	);
#
#	CREATE INDEX api_extensiones_sip__idx__commented ON api_extensiones_sip(commented);
#
##############################################################################
#Creamos los campos adicionales Nombre y apellidos para darle un valor al 'callerid'
#con el siguiente formato -> "Nomre Apellidos" <extension>
	nombre = models.CharField(max_length=80,null=True)
	apellidos = models.CharField(max_length=80,null=True)	
 
#       callerid VARCHAR(80) DEFAULT NULL,
        callerid = models.CharField(max_length=80,null=True,blank=True)

#       username VARCHAR(80) NOT NULL DEFAULT '',
        username = models.CharField(max_length=80,verbose_name='Usuario')

#       name VARCHAR(80) NOT NULL DEFAULT '',
	name = models.CharField(max_length=80,verbose_name='Extension')
#       secret VARCHAR(80) DEFAULT NULL, 
        secret = models.CharField(max_length=80,null=True,verbose_name='Clave')
#       language CHAR(2) DEFAULT NULL,
        ##Idiomas definidos en /etc/asterisk/indications.conf
        ##Por defecto 'es'
        language = models.CharField(max_length=2,default='es',blank=True,verbose_name='Idioma')
 
#       host VARCHAR(31) NOT NULL DEFAULT '', 
	host = models.CharField(max_length=31,default='dynamic')
#       nat VARCHAR(5) NOT NULL DEFAULT 'no',
	NAT_CHOICES = (
                       ('yes','yes'),
                       ('no','no'),
                       ('route','route'),
                       ('never','never'),
                      )
	nat = models.CharField(max_length=5,choices=NAT_CHOICES,default='no') 
#       type VARCHAR(6) NOT NULL DEFAULT 'friend',
	TYPE_CHOICES = (
                        ('friend','friend'),
                        ('user','user'),
                        ('peer','peer'),
                       )
	type = models.CharField(max_length=6,choices=TYPE_CHOICES,default='friend') 
#       accountcode VARCHAR(20) DEFAULT NULL,
	accountcode = models.CharField(max_length=20,null=True,blank=True) 
#       amaflags VARCHAR(13) DEFAULT NULL,
	AMAFLAGS_CHOICES = (
                        ('default','default'),
                        ('omit','omit'),
                        ('billing','billing'),
                        ('documentation','documentation'),
                       )

	amaflags = models.CharField(max_length=13,null=True,choices=AMAFLAGS_CHOICES,default='default') 
#       callgroup VARCHAR(10) DEFAULT NULL,
	callgroup = models.CharField(max_length=10,null=True,blank=True) 
#       cancallforward CHAR(3) DEFAULT 'yes',
	YES_NO_CHOICES =(
                        ('yes','yes'),                        
                        ('no','no'),
                        )
	cancallforward = models.CharField(max_length=3,choices=YES_NO_CHOICES,default='yes') 
#       directmedia CHAR(3) DEFAULT 'yes',
	directmedia = models.CharField(max_length=3,choices=YES_NO_CHOICES,default='yes')
 
#       context VARCHAR(80) DEFAULT NULL,
	CONTEXTOS = [( c['context'], c['context'] ) for c in linea.objects.values('context').distinct() ]


	context = models.CharField(max_length=50,choices=CONTEXTOS, verbose_name='Contexto')


	#context = models.CharField(max_length=80,null=True,verbose_name='Contexto') 

#       defaultip VARCHAR(15) DEFAULT NULL,
	defaultip = models.CharField(max_length=15,null=True,blank=True) 
#       dtmfmode VARCHAR(7) DEFAULT NULL,
	DTMFMODE_CHOICES =(
                           ('rfc2833','rfc2833'),
                           ('info','info'),
                           ('inband','inband'),
                           ('auto','auto'),
                        )

	dtmfmode = models.CharField(max_length=7,null=True,choices=DTMFMODE_CHOICES,default='rfc2833') 
#       fromuser VARCHAR(80) DEFAULT NULL,
	fromuser = models.CharField(max_length=80,null=True,blank=True) 
#       fromdomain VARCHAR(80) DEFAULT NULL,
	fromdomain = models.CharField(max_length=80,null=True,blank=True) 
#       insecure VARCHAR(4) DEFAULT NULL,
	insecure = models.CharField(max_length=4,null=True,default='no',blank=True) 
#       mailbox VARCHAR(50) DEFAULT NULL,
	mailbox = models.CharField(max_length=50,null=True,blank=True) 
#       md5secret VARCHAR(80) DEFAULT NULL,
#################################################################################
#	Syntax:
#	md5secret=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

#	where xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx is the md5hash of "<user>:asterisk:<secret>"

#	Description:
#	Use this option if you don't want to have plaintext-passwords in your sip.conf. You can build the md5hash with

#	echo -n "<user>:<realm>:<secret>" | md5sum

#	The <realm> is "asterisk" by default. If you've set it, use the realm you configured.

#	The -n is important because otherwise echo will add a \n at the end of the string and the md5hash would be totally different.

#	If there is an md5secret for a user in the config, the secret for that user will be ignored!

#	Example:
#	To generate the md5-hash for user 1234 with secret abcd you do:

#	echo -n "1234:asterisk:abcd" | md5sum

#	and as result you should get

#	4a8e71480c5b1ef0a5d502a8eb98576a
## Info sacada de http://www.voip-info.org/wiki/view/Asterisk+sip+md5secret
########################################################################################
	md5secret = models.CharField(max_length=80,null=True,blank=True) 
#       deny VARCHAR(95) DEFAULT NULL,
	deny = models.CharField(max_length=95,null=True,blank=True) 
#       permit VARCHAR(95) DEFAULT NULL,
	permit = models.CharField(max_length=95,null=True,blank=True) 
#       mask VARCHAR(95) DEFAULT NULL,
	mask = models.CharField(max_length=95,null=True,blank=True)
#       musiconhold VARCHAR(100) DEFAULT NULL,
#	Una de las clases especificadas en /etc/asterisk/musiconhold.conf
	musiconhold = models.CharField(max_length=100,null=True,blank=True) 
#       pickupgroup VARCHAR(10) DEFAULT NULL,
	pickupgroup = models.CharField(max_length=10,null=True,blank=True) 
#       qualify CHAR(3) DEFAULT NULL,
#	Syntax:
#
#	qualify=xxx|no|yes
#
#	where xxx is the number of milliseconds used. If yes the default timeout is used, 2 seconds.
	qualify = models.CharField(max_length=3,null=True,default='yes',blank=True) 
#       regexten VARCHAR(80) DEFAULT NULL,
	regexten = models.CharField(max_length=80,null=True,blank=True) 
#       restrictcid CHAR(3) DEFAULT NULL, 
	restrictcid = models.CharField(max_length=3,null=True,choices=YES_NO_CHOICES,default='no')
#       rtptimeout CHAR(3) DEFAULT NULL,
#	Terminate call if 60 seconds of no RTP activity when we're not on hold 
	rtptimeout = models.CharField(max_length=3,null=True,default=60,blank=True)
#       rtpholdtimeout CHAR(3) DEFAULT NULL,
#	Terminate call if 300 seconds of no RTP activity when we're on hold (must be > rtptimeout) 
	rtpholdtimeout = models.CharField(max_length=3,null=True,default=300,blank=True)
#       setvar VARCHAR(100) DEFAULT NULL, 
	setvar = models.CharField(max_length=100,null=True,blank=True)
#       disallow VARCHAR(100) DEFAULT 'all',
#	First disallow all codecs 
	disallow = models.CharField(max_length=100,null=True,default='all',blank=True)
#       allow VARCHAR(100) DEFAULT 'g729,ilbc,gsm,ulaw,alaw',
	allow = models.CharField(max_length=100,null=True,default='g729,ilbc,gsm,ulaw,alaw',blank=True) 
#       fullcontact VARCHAR(80) NOT NULL DEFAULT '',
#	<sip:uri_contact> : SIP URI contact for realtime peer. Valid only for realtime peers. 
	fullcontact = models.CharField(max_length=80,blank=True)
#       ipaddr VARCHAR(15) NOT NULL DEFAULT '',
#	Dotted Quad IP address of the peer. Valid only for realtime peers.
	ipaddr = models.CharField(max_length=15,blank=True) 
#       port INT(11) NOT NULL DEFAULT 0, 
#	SIP port of the client
	port = models.IntegerField(default=0,null=True,blank=True)
#       regserver VARCHAR(100) DEFAULT NULL,
	regserver = models.CharField(max_length=100,null=True,blank=True) 
#       regseconds INT(11) NOT NULL DEFAULT 0,
#	seconds : Number of seconds between SIP REGISTER. Valid only for realtime peer entries
	regseconds = models.IntegerField(default=0,blank=True) 

	##Definimos la forma de mostrar los datos al hacer una consulta,
	##Para ello creamos la funcion __str__(self)
	def __str__(self):
		return '%s %s %s %s %s' % (self.nombre,self.apellidos,self.callerid,self.username,self.name)

	def __unicode__(self):
		return '%s %s %s %s' %(self.nombre,self.apellidos,self.username,self.name, self.secret)


#Documentacion para crear un formulario a partir de un modelo
#https://docs.djangoproject.com/en/1.5/topics/forms/modelforms/

#class BookForm(ModelForm):
#    class Meta:
#        model = Book
#Creamos dos formularios, uno para los atributos requeridos para crear la extension
#y otro para los demas parametros no requeridos


class sipUserFormPer(ModelForm):
	class Meta:
		#Ponemos el input callerid oculto
		callerid = forms.CharField(widget=forms.HiddenInput)
		widgets = {
                           'callerid' : forms.HiddenInput(),
                          } 

		#Creamos el formulario a partir del modelo definido con los atributos especificados en fields
		model = sip
		fields = ('nombre','apellidos','name','callerid')

class sipUserFormAco(ModelForm):
	class Meta:
		#####MODIFICACION DE ATRIBUTOS DEL FORMULARIO###############
		#Modificamos el campo secret para generar un input tipo password
		secret = forms.CharField(widget=forms.PasswordInput)
		
		#Y Ponemos el input username de solo lectura, ya que se rellenara automaticamente 
                #con el mismo valor que la extension
		username = forms.CharField(widget=forms.TextInput) 
		
		widgets = {
                           'secret' : forms.PasswordInput(),
                           'username' : forms.TextInput(attrs={'readonly':'readonly',}),
                          }
                ##############################################################

		model = sip
		fields = ('username','secret','context','language')


class ConfirPassForm(forms.Form):
	#Creamos un campo adicional en el formulario para confirmar la clave
	confirma = forms.CharField(widget=forms.PasswordInput)
	widgets = {
                   'confirma' : forms.PasswordInput(),
                  }
	#Incluimos una regla de validacion  -> NO FUNCIONA MIRAR
	#def clean_message(self):
	#	datos = self.clean_data.get('confirma')
	#	if datos == 'pepe':
	#		raise forms.ValidationError('La confirmacion de clave no puede ser nula')
	#	return datos

class sipOptionForm(ModelForm):
	class Meta:
		model = sip
		exclude = ('nombre','apellidos','username','callerid','name','secret','context','language')

##Creamos una formulario con todos loas campos necesario para la hora de guardarlo con save()
class sipForm(ModelForm):
	class Meta:
		model = sip



##############################################################################################################
#####################################################EXTENSIONES IAX###########################################
##############################################################################################################


class iax(models.Model):

	
	YES_NO_CHOICES =(
                        ('yes','yes'),
                        ('no','no'),
                        )

#Creamos los campos adicionales Nombre y apellidos para darle un valor al 'callerid'
#con el siguiente formato -> "Nomre Apellidos" <extension>
	nombre = models.CharField(max_length=80,null=True)
	apellidos = models.CharField(max_length=80,null=True)

#       callerid VARCHAR(80) DEFAULT NULL,
	callerid = models.CharField(max_length=80,null=True,blank=True)

#       username VARCHAR(80) NOT NULL DEFAULT '',
	username = models.CharField(max_length=80,verbose_name='Usuario')

#      "name" varchar(80) PRIMARY KEY NOT NULL,
	name = models.CharField(max_length=80,primary_key=True,verbose_name='Extension')

#       type VARCHAR(6) NOT NULL DEFAULT 'friend',
	TYPE_CHOICES = (
                        ('friend','friend'),
                        ('user','user'),
                        ('peer','peer'),
                       )
        type = models.CharField(max_length=6,choices=TYPE_CHOICES,default='friend')

#	secret VARCHAR(80) DEFAULT NULL, 
	secret = models.CharField(max_length=80,null=True,verbose_name='Clave')
	
	md5secret = models.CharField(max_length=80,null=True,blank=True)

	dbsecret = models.CharField(max_length=100,null=True,blank=True)

	notransfer = models.CharField(max_length=10,null=True,blank=True)

	inkeys = models.CharField(max_length=100,null=True,blank=True)

	outkeys = models.CharField(max_length=100,null=True,blank=True)

	auth = models.CharField(max_length=100,null=True,blank=True)

	accountcode = models.CharField(max_length=100,null=True,blank=True)

#       amaflags VARCHAR(13) DEFAULT NULL,
	AMAFLAGS_CHOICES = (
                        ('default','default'),
                        ('omit','omit'),
                        ('billing','billing'),
                        ('documentation','documentation'),
                       )

	amaflags = models.CharField(max_length=13,null=True,choices=AMAFLAGS_CHOICES,default='default')

#       context VARCHAR(80) DEFAULT NULL,
	CONTEXTOS = [( c['context'], c['context'] ) for c in linea.objects.values('context').distinct() ]

        context = models.CharField(max_length=50,choices=CONTEXTOS, verbose_name='Contexto')

#       defaultip VARCHAR(15) DEFAULT NULL,
	defaultip = models.CharField(max_length=15,null=True,blank=True)

#	host varchar(31) NOT NULL default 'dynamic',
	host = models.CharField(max_length=31,default='dynamic')

	language = models.CharField(max_length=2,default='es',blank=True,verbose_name='Idioma')

#       mailbox VARCHAR(50) DEFAULT NULL,
	mailbox = models.CharField(max_length=50,null=True,blank=True)

#       deny VARCHAR(95) DEFAULT NULL,
	deny = models.CharField(max_length=95,null=True,blank=True)
#       permit VARCHAR(95) DEFAULT NULL,
	permit = models.CharField(max_length=95,null=True,blank=True)

#       qualify CHAR(3) DEFAULT NULL,
#       Syntax:
#
#       qualify=xxx|no|yes
#
#       where xxx is the number of milliseconds used. If yes the default timeout is used, 2 seconds.
	qualify = models.CharField(max_length=3,null=True,default='no',blank=True)

#       disallow VARCHAR(100) DEFAULT 'all',
#       First disallow all codecs 
	disallow = models.CharField(max_length=100,null=True,default='all',blank=True)
#       allow VARCHAR(100) DEFAULT 'g729,ilbc,gsm,ulaw,alaw',
	allow = models.CharField(max_length=100,null=True,default='alaw,g729,ilbc,gsm,ulaw',blank=True)

#       ipaddr VARCHAR(15) NOT NULL DEFAULT '',
#       Dotted Quad IP address of the peer. Valid only for realtime peers.
	ipaddr = models.CharField(max_length=15,blank=True,null=True)
#       port INT(11) NOT NULL DEFAULT 0, 
#       IAX port of the client
	port = models.IntegerField(blank=True,default=4569)

#       regseconds INT(11) NOT NULL DEFAULT 0,
#       seconds : Number of seconds between IAX REGISTER. Valid only for realtime peer entries
	regseconds = models.IntegerField(default=0,blank=True)

	requirecalltoken = models.CharField(max_length=15,default='auto')

##Creamos una formulario con todos los campos del modelo iax
class iaxForm(ModelForm):
        class Meta:
                model = iax
	#	exclude = ('name')

class iaxUserFormPer(ModelForm):
        class Meta:
                #Ponemos el input callerid oculto
		callerid = forms.CharField(widget=forms.HiddenInput)
		widgets = {
                           'callerid' : forms.HiddenInput(),
                          }

                #Creamos el formulario a partir del modelo definido con los atributos especificados en fields
		model = iax
		fields = ('nombre','apellidos','name','callerid')


class iaxUserFormAco(ModelForm):
        class Meta:
                #####MODIFICACION DE ATRIBUTOS DEL FORMULARIO###############
                #Modificamos el campo secret para generar un input tipo password
		secret = forms.CharField(widget=forms.PasswordInput)

                #Y Ponemos el input username de solo lectura, ya que se rellenara automaticamente 
                #con el mismo valor que la extension
		username = forms.CharField(widget=forms.TextInput)

		widgets = {
                           'secret' : forms.PasswordInput(),
                           'username' : forms.TextInput(attrs={'readonly':'readonly',}),
                          }
                ##############################################################

		model = iax
		fields = ('username','secret','context','language')


class iaxOptionForm(ModelForm):
	class Meta:
		model = iax
		exclude = ('nombre','apellidos','username','callerid','name','secret','context','language')

