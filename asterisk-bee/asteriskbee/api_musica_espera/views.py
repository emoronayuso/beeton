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
def admin_moh(request):

	lista_archivos = moh.objects.all()

	if request.method == 'POST':

		formulario_upload_audio = MohForm(request.POST, request.FILES)

                ##Comprobamos que los campos no sean nulos y sean de acuerdo al tipo definido
		if formulario_upload_audio.is_valid():
			
			formulario_upload_audio.save()

			##Una vez guardada en la base de datos le damos el valor al atributo application
			m = moh.objects.get(name=request.POST.get('name'))
			nombre_fichero = str(m.fichero_audio).split('/')[2]
			m.nombre_mp3 = nombre_fichero   
			m.application = '/usr/bin/mpg123 -q -r 8000 -f 8192 -s --mono '+nombre_fichero
			m.save()

			return HttpResponseRedirect('/admin/moh/')

	else:

		formulario_upload_audio = MohForm()

	return render_to_response('moh/moh.html',{'lista_archivos' : lista_archivos, 'form_upload_audio': formulario_upload_audio },context_instance=RequestContext(request))



##Funcion que borra un fichero de audio
@login_required(login_url='/login')
def borra_moh(request):

	name_audio = request.GET.get('name_audio')

	audio_sele = moh.objects.get(name=name_audio)

        #Eliminamos el fichero de audio primero
	default_storage.delete(audio_sele.fichero_audio.path)

        #Por ultimo la tupla correspondiente de la base de datos
	audio_sele.delete()

        #Devolvemos la nueva lista sin el audio eliminado
	lista_audio = moh.objects.all()

	return render_to_response('moh/lista_moh.html',{ 'lista_archivos': lista_audio },context_instance=RequestContext(request))


