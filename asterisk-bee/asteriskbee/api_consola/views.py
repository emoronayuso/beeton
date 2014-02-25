#encoding:utf-8
from django.shortcuts import render_to_response

#Para uso de la funcion HttpResponseRedirect (redireccionar paginas)
from django.http import HttpResponseRedirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django.template import RequestContext
from django.conf import settings

#Herramientas de DEBUG de python####
import pdb

########modulo para ejecutar comandos en la shell####
### COMANDO PARA EJECUTAR -> 'asterisk -x <comando consola >'
### -x implica -r

import subprocess

from asteriskbee.api_consola.forms import consola_form
from models import *


@login_required(login_url='/login/')
def consola(request):
	usuario=request.user
	co_aux=''
	co_aux2='' 

	tam_max_historial = 50
	tam_his = historial_comandos.objects.all().count()
	
	if request.GET:
		
		comando = request.GET['comando']
		##################Guardamos el comando en el historial########
	#	tam_his = historial_comandos.objects.all().count()
		h = historial_comandos()
		historial = historial_comandos.objects.all()
		if tam_his == 0:
			h.comando = comando
			h.save()
		elif tam_his == 1:
			h.comando = comando
			h.save()
			
			c = historial_comandos.objects.get(id=1)
			co_aux = c.comando
			c.comando = comando		
			c.save()
			
			c = historial_comandos.objects.get(id=2)
			c.comando = co_aux
			c.save()
		else:
			for c in historial:
				if c.id==1:
					co_aux = c.comando 
					c.comando = comando
				else:
					co_aux2 = c.comando
					c.comando = co_aux
					co_aux = co_aux2
				c.save()
			if tam_his < tam_max_historial:
				h.comando = co_aux2
				h.save()
			
				
		#############################################################
		
		# Creamos los descriptores de archivos
		# con permisos de escritura llamados 'archivo_out' y 'archivo_err'
       		# + para poder leer y escribir simultaneamente
		outfd = open(settings.STATIC_ROOT+'api_consola/archivos/archivo_out', 'w+')
		errfd = open(settings.STATIC_ROOT+'api_consola/archivos/archivo_err', 'w+')

	#	formulario = consola_form(request.GET)
		formulario = historialComandosForm()	
	
		comando = request.GET['comando']

        # Ejecutamos el comando especificado y guardamos la salida en los ficheros
		subprocess.call(['asterisk', '-x', comando], stdout=outfd, stderr=errfd)

        # Cerramos los archivos para que se escriban los cambios y se liberen
        # los buffers de I/O
		outfd.close()
		errfd.close()

        # Ahora leemos todo lo que tengan los archivos y guardamos en la variable
        # output la salida estándar y en err la salida de error.
	fd = open(settings.STATIC_ROOT+'api_consola/archivos/archivo_out', 'r')

        output= fd.readlines()
	
	fd.close()

	fd = open(settings.STATIC_ROOT+'api_consola/archivos/archivo_err', 'r')
	err = fd.read()


	formulario = consola_form()

	id_comando = 0

	return render_to_response('consola/consola.html',{'tam_historial': tam_his ,'id_comando' : id_comando,'formulario_consola': formulario , 'salida_consola':output, 'salida_consola_error':err},context_instance=RequestContext(request))



def histo_comandos(request):

	comando_sele =''
	h_comandos =  historial_comandos.objects.all()
	
	if request.GET:
		comando_s =  h_comandos.get(id=request.GET['id_historial_comando'])
		comando_sele = comando_s.comando


	return render_to_response('consola/form_consola.html',{ 'comando_sele' : comando_sele },context_instance=RequestContext(request))

