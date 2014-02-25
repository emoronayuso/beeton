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
from asteriskbee.api_dialplan.models import aplicaciones
#######from models import linea

#Herramientas de DEBUG de python####
import pdb

###USO: pdb.set_trace()
###(pdb) <pulsar n para siguiente>

#Funcion que permite tratar con ficheros
from django.core.files.storage import default_storage

#libreria del sistema para ejecutar comandos
import os

from django.conf import settings

import json

#Funcion que muestra la lista de las extensiones sip
@login_required(login_url='/login')
def add_func(request):

        lista_app =  aplicaciones.objects.values('nombre')

        if request.method == 'POST':

                formulario_upload_func = funcForm(request.POST, request.FILES)

                ##Comprobamos que los campos no sean nulos y sean de acuerdo al tipo definido
                if formulario_upload_func.is_valid():

                        formulario_upload_func.save()

			#request.FILES.get('fichero_tar_gz')

			#settings.STATIC_ROOT --> /home/asterisk-bee/asteriskbee/
			##Descomprimimos el fichero e la carpeta temp
			os.system("tar -xzvf "+settings.STATIC_ROOT+"api_admin_func/pkg_instalados/"+str(request.FILES.get('fichero_tar_gz'))+" -C "+settings.STATIC_ROOT+"api_admin_func/pkg_instalados/temp/")
# Create your views here.
			
			##Una vez descomprimido abrimos el fichero json para insertar los datos en la base de datos
			os.system("ls "+settings.STATIC_ROOT+'api_admin_func/pkg_instalados/temp/'+" | grep -e '.json' >"+settings.STATIC_ROOT+'api_admin_func/pkg_instalados/temp/nombre_fich')
			f = open(settings.STATIC_ROOT+'api_admin_func/pkg_instalados/temp/nombre_fich','r')
			nombre_fich_json = f.readline().strip()		
			f.close()

	
			#pdb.set_trace()
			with open(settings.STATIC_ROOT+'api_admin_func/pkg_instalados/temp/'+nombre_fich_json) as data_file:
				data = json.load(data_file)		
	
			#pdb.set_trace()
			##Una vez leido el fichero json, insertamos las valores en la tabla de aplicaciones
			a = aplicaciones(nombre=data["aplicacion"]["nombre"],descripcion=data["aplicacion"]["descripcion"],script=data["aplicacion"]["script"],num_para=int(data["aplicacion"]["num_para"]),color=data["aplicacion"]["color"],nom_arch_temp=data["aplicacion"]["nom_arch_temp"], temp_param1=int(data["aplicacion"]["temp_param1"]),nom_param1=data["aplicacion"]["nom_param1"], des_param1=data["aplicacion"]["des_param1"], temp_param2=int(data["aplicacion"]["temp_param2"]),nom_param2=data["aplicacion"]["nom_param2"],des_param2=data["aplicacion"]["des_param2"], temp_param3=int(data["aplicacion"]["temp_param3"]),nom_param3=data["aplicacion"]["nom_param3"],des_param3=data["aplicacion"]["des_param3"],temp_param4=int(data["aplicacion"]["temp_param4"]),nom_param4=data["aplicacion"]["nom_param4"],des_param4=data["aplicacion"]["des_param4"],temp_param5=int(data["aplicacion"]["temp_param5"]),nom_param5=data["aplicacion"]["nom_param5"],des_param5=data["aplicacion"]["des_param5"],temp_param6=int(data["aplicacion"]["temp_param6"]),nom_param6=data["aplicacion"]["nom_param6"],des_param6=data["aplicacion"]["des_param6"],temp_param7=int(data["aplicacion"]["temp_param7"]),nom_param7=data["aplicacion"]["nom_param7"],des_param7=data["aplicacion"]["des_param7"],temp_param8=int(data["aplicacion"]["temp_param8"]),nom_param8=data["aplicacion"]["nom_param8"],des_param8=data["aplicacion"]["des_param8"],temp_param9=int(data["aplicacion"]["temp_param9"]),nom_param9=data["aplicacion"]["nom_param9"],des_param9=data["aplicacion"]["des_param9"], temp_param10=int(data["aplicacion"]["temp_param10"]),nom_param10=data["aplicacion"]["nom_param10"],des_param10=data["aplicacion"]["des_param10"]  )

			a.save()
			
			data_file.close()
			##Una vez leido el fichero json lo borramos de la carpeta temporal
			os.system("rm "+settings.STATIC_ROOT+'api_admin_func/pkg_instalados/temp/'+nombre_fich_json)


			##Movemos los archivos de la app en sus carpetas correspondientes######################
                        nombre_fich_py = nombre_fichero('py')
			
			os.system("mv "+settings.STATIC_ROOT+'api_admin_func/pkg_instalados/temp/'+nombre_fich_py+" "+settings.STATIC_ROOT+'agi_bin/'+nombre_fich_py)

			
			nombre_fich_html = nombre_fichero('html')

			if nombre_fich_html != "":
				os.system("mv "+settings.STATIC_ROOT+'api_admin_func/pkg_instalados/temp/'+nombre_fich_html+" "+settings.STATIC_ROOT+'templates/dialplan/temp_api_instaladas/'+nombre_fich_html)
			
			nombre_fich_js = nombre_fichero('js')

			if nombre_fich_js != "":
				os.system("mv "+settings.STATIC_ROOT+'api_admin_func/pkg_instalados/temp/'+nombre_fich_js+" "+settings.STATIC_ROOT+'templates/js/'+nombre_fich_js)

				##Si existe el fichero javascript tenemos que incluir la linea en al fichero js base
				fichero_js_base = open(settings.STATIC_ROOT+'templates/js/refresca_div.js', 'a')
				fichero_js_base.write("document.write(\"<script src = \'/js/"+nombre_fich_js+"\' language = 'JavaScript' type = 'text/javascript'></script>\");")
				fichero_js_base.close()
			#######################################################################################

                        return HttpResponseRedirect('/admin/admin_func/')

        else:

                formulario_upload_func = funcForm()

        return render_to_response('admin_func/admin_func.html',{'lista_app' : lista_app, 'form_upload_func': formulario_upload_func },context_instance=RequestContext(request))


def nombre_fichero(extension):

	nombre_fich = ""

	os.system("ls "+settings.STATIC_ROOT+'api_admin_func/pkg_instalados/temp/'+" | grep -e ."+extension+"$ >"+settings.STATIC_ROOT+'api_admin_func/pkg_instalados/temp/nombre_fich')
	f = open(settings.STATIC_ROOT+'api_admin_func/pkg_instalados/temp/nombre_fich','r')
	nombre_fich = f.readline().strip()
	f.close()

	return nombre_fich


