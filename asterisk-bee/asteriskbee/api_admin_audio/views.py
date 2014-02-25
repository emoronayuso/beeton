# Create your views here.

#encoding:utf-8
from django.shortcuts import render_to_response

#Para uso de la funcion HttpResponseRedirect (redireccionar paginas)
from django.http import HttpResponseRedirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django.template import RequestContext
#from django.conf import settings

#Incluimos el modelo para poder crear los formularios
from models import *
#######from models import linea

#Herramientas de DEBUG de python####
import pdb

###USO: pdb.set_trace()
###(pdb) <pulsar n para siguiente>

#Funcion que permite tratar con ficheros
from django.core.files.storage import default_storage

#Funcion que muestra la lista de las extensiones sip
@login_required(login_url='/login')
def admin_audio(request):

	lista_archivos = ficheros_audio.objects.all()
  
	if request.method == 'POST':

		formulario_upload_audio = ficheroAudioForm(request.POST, request.FILES)

                ##Comprobamos que los campos no sean nulos y sean de acuerdo al tipo definido
		if formulario_upload_audio.is_valid():
			
			formulario_upload_audio.save()		

			return HttpResponseRedirect('/admin/admin_audio/')

	else:

        	formulario_upload_audio = ficheroAudioForm()

        return render_to_response('admin_audio/admin_audio.html',{'lista_archivos' : lista_archivos, 'form_upload_audio': formulario_upload_audio },context_instance=RequestContext(request))


##Funcion que borra un fichero de audio
@login_required(login_url='/login')
def borra_audio(request):

	id_audio = request.GET.get('id_audio')

	audio_sele = ficheros_audio.objects.get(id=id_audio)

	#Eliminamos el fichero de audio primero
	default_storage.delete(audio_sele.fichero_audio.path)

	#Por ultimo la tupla correspondiente de la base de datos
	audio_sele.delete()

	#Devolvemos la nueva lista sin el audio eliminado
	lista_audio = ficheros_audio.objects.all()

	return render_to_response('admin_audio/lista_audio.html',{ 'lista_archivos': lista_audio },context_instance=RequestContext(request))

	#return admin_audio(request)

