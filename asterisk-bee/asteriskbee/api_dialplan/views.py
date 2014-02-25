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

import sets

#Incluimos el modelo ficheros_audio y de moh
from asteriskbee.api_admin_audio.models import ficheros_audio
from asteriskbee.api_musica_espera.models import moh

#Herramientas de DEBUG de python####
import pdb

###USO: pdb.set_trace()
###(pdb) <pulsar n para siguiente>

########modulo para ejecutar comandos en la shell####
### COMANDO PARA EJECUTAR -> echo '[nombre_contexto]' >> /etc/asterisk/extensions.conf
### y --> echo 'switch => Realtime/@' >> /etc/asterisk/extensions.conf
### -x implica -r

import subprocess



#Funcion que muestra la lista de las extensiones sip
@login_required(login_url='/login')
def lista_contextos(request):

	mapa_contextos = {}
	
	##Sacamos la lista de contexto de las lineas del dialplan
	mapa = linea.objects.values('context').distinct()

	#Creamos un diccionario para gestionar los contextos
        for contexto in mapa:
                mapa_contextos[contexto['context']] = contexto['context']

        return render_to_response('dialplan/dialplan.html',{'mapa_contextos' : mapa_contextos },context_instance=RequestContext(request))


@login_required(login_url='/login')
def add_contexto(request):

	if request.method == 'POST':

		contexto_form = contextoForm(request.POST)

		##Comprobamos que los campos no sean nulos y sean de acuerdo al tipo definido
		if contexto_form.is_valid():

			#Guardamos TODOS los datos en la base de datos y redirigimos
#			contexto_form.save()

			##Antes de incluir las lineas en el fichero de configuracion del dialplan 
                        ##/etc/asterisk/extensions.conf:
                        ## [nombre_del_contexto]
                        ## switch => Realtime/@ 

		        ##Debemos comprobar aqui que no existen dos contextos con el mismo nombre
			###    QUEDA PENDIENTE #####

                        ###Incluimos las lineas en el dialplan para indicar a Asterisk que 
		        ###usara la configuracion de la base de datos del Realtime
			
			##Creamos el manejador de ficheros en modo anadir 'a'
			fichero_extensions = open('/etc/asterisk/extensions.conf', 'a')		        

			contexto = request.POST.get('context')
			
			##Escribimos en el fichero
			fichero_extensions.write("["+contexto+"]\nswitch => Realtime/@\n")

		        # Cerramos en archivo 
			fichero_extensions.close()

			##Ahora solo quedaria crear una primera linea de contexto, por ejemplo para la extension 1 usando la aplicacion espera
			l = linea(context=contexto,exten=1,priority=1,appdata='esperar.py')
			l.save()
			api = aplicaciones.objects.get(script='esperar.py')
			param = parametros(id_linea=l,id_api=api,param1=1)
			param.save()
	
			return HttpResponseRedirect('/admin/dialplan/')

	else:

		contexto_form = contextoForm

		lista = {}	
	
	return render_to_response('dialplan/crear_contexto.html',{'lista_contextos' : lista, 'formulario_contexto' : contexto_form },context_instance=RequestContext(request))



###Funcion que visualiza las lineas del contexto seleccionado, y permite modificar cada una
@login_required(login_url='/login')
def mod_contexto(request):

	##Lo primero sera listar las lineas del contexto selecciondo

	contexto_sele = request.GET.get('context')

	##Realizamos una consulta de todas las lineas que tienen el contexto seleccionado
	lineas_sele = linea.objects.filter(context=contexto_sele)


	linea_sele = {}

	linea_form = {}

	aplicacion_form = {}
	aplicacion_nom_param_form = {}
	aplicaciones_des_param_form = {}
	aplicacion_acti_temp_param_form = {}

	add_linea = {}

	lista_api = aplicaciones.objects.all()

	lista_contextos = linea.objects.values('context').distinct()

	parametros_form = {}

	datos_api = {}
	
	########Modificar si en un fururo se incluyen mas parametros para las aplicaciones##########
	num_param = 10#############################################################################
	###########################################################################################

	id_api = {}
	nombre_api = {}

	lista_audios = ficheros_audio.objects.all()

	mapa_audio = {}
	for audio in lista_audios:
		ls1 = str(audio.fichero_audio).split('/')
		ls2 = ls1[1].split('.')
		
		opc = ls2[0]

		mapa_audio[str(audio.nombre)]= opc
	
	lista_opciones = mapa_audio.keys()
	lista_valor_ast = mapa_audio.values()

	mohs = moh.objects.all()
	
	lista_moh = {}

	for m in mohs:
		lista_moh[str(m.name)] = str(m.name)

	lista_moh = lista_moh.values()

	#pdb.set_trace() 
################################Si se ha seleccionado MODIFICAR alguna linea#########################################
	if request.GET.get('id_linea'):
		#Sacamos las id de la linea seleccionada
	        id_linea_sele = request.GET.get('id_linea')

		linea_sele = linea.objects.filter(id=id_linea_sele)

		##Mostramos el formulario para modificar la linea
		##Si se pulsa sobre la opcion 'modificar linea' de la linea seleccionada
		if request.method == 'POST':		
			##Recogemos los datos de los formularios linea y parametros
	
			##INSTANCIANDOLOS ANTES, ya que si no se crearia una linea nueva. IMPORTANTE!!!!
                        datos_linea = linea.objects.get(pk=id_linea_sele)
			linea_form = lineaContextoForm(request.POST, instance=datos_linea)

			####HACEMOS LO MISMO CON EL FORMULARIO DE PARAMETROS			
			datos_param = parametros.objects.get(id_linea=id_linea_sele)
                        parametros_form = parametrosLineaContextoForm(request.POST,instance=datos_param)
	
			#linea_form = lineaContextoForm(request.POST)
			#parametros_form = parametrosLineaContextoForm(request.POST)
			

                	##Comprobamos que los campos no sean nulos y sean de acuerdo al tipo definido
			if linea_form.is_valid() and parametros_form.is_valid():

				##NOTA: NO HACE FALTA RECOGER TODOS LOS DATOS PARA MODIFICAR LA LINEA###
				exten = linea_form.cleaned_data['exten']
				##########################################################
				
				##################TODOS LOS VALORES DE TODOS LOS PARAMETROS##########
				param1 = parametros_form.cleaned_data['param1']
				param2 = parametros_form.cleaned_data['param2']
				param3 = parametros_form.cleaned_data['param3']
				param4 = parametros_form.cleaned_data['param4']
				param5 = parametros_form.cleaned_data['param5']
				param6 = parametros_form.cleaned_data['param6']
				param7 = parametros_form.cleaned_data['param7']
				param8 = parametros_form.cleaned_data['param8']
				param9 = parametros_form.cleaned_data['param9']
				param10 = parametros_form.cleaned_data['param10']
				####################################################################

				#Guardamos TODOS los datos en la base de datos y redirigimos
				linea_form.save()
				parametros_form.save()

                        return HttpResponseRedirect('/admin/dialplan/mod_contexto/?context='+contexto_sele)


		else:
			###Mostramos los formularios con los datos para modificar una linea
			datos_linea = linea.objects.get(pk=request.GET.get('id_linea'))
			##Este formulario solo muestra el numero de extension de la linea
			linea_form = lineaContextoForm(instance=datos_linea)
		
			##Mostramos la lista de aplicaciones disponibles
#			lista_api = aplicaciones.objects.all()

			datos_param = parametros.objects.get(id_linea=id_linea_sele)
			##Sacamos la lista de parametros a partir de la llinea seleccionada
			parametros_form = parametrosLineaContextoForm(instance=datos_param) 		
	
			###A partir del modelo parametros sacamos la aplicacion y su formulario
			#datos_api = aplicaciones.objects.get(datos_param.id_api) 
			datos_api = datos_param.id_api
			
			num_param = datos_api.num_para

			aplicacion_form = aplicacionContextoForm(instance=datos_api)

			####Sacamos los formularios con los nombres,las descripciones y si la aplicacion tiene o noplantilla para cada parametro
			aplicacion_nom_param_form = aplicacionContextoParamForm(instance=datos_api)
			aplicaciones_des_param_form = aplicacionContextoDesParamForm(instance=datos_api)
			aplicacion_acti_temp_param_form = aplicacionBitActTemplateParamForm(instance=datos_api)
####################################################FIN MODIFICAR LINEA###########################################




	

###################################################ANADIR NUEVA LINEA##############################################
	##Si se ha seleccionado anadir una nueva linea en el contexto
	if request.GET.get('add_linea'):
		##Esta linea es para seleccionar el div del formulario para anadir nueva linea en la plantilla
		add_linea = 1

		linea_form = lineaContextoForm
		
		##Mostramos la lista de aplicaciones disponibles
		lista_api = aplicaciones.objects.all()

		lista_contextos = linea.objects.values('context').distinct()

                ###Sacamos los datos de la aplicacion por defecto seleccionada RESPONDER_LLAMADAS con id 1
                datos_api = aplicaciones.objects.get(id=1) 

		id_api = datos_api.id
		nombre_api = datos_api.nombre
	
		#Sacamos el numero de parametros de la aplicacion seleccionada por defecto
		num_param = datos_api.num_para
	
		#Generamos el formulario de los datos de la aplicacion de la api seleccionada por defecto
		aplicacion_form = aplicacionContextoForm(instance=datos_api)

		#Sacamos el formulario de los parametros de la aplicacion seleccionada por defecto
		parametros_form = parametrosLineaContextoForm()	
                ####Sacamos los formularios con los nombres y las descripciones de la aplicacion
		aplicacion_nom_param_form = aplicacionContextoParamForm(instance=datos_api)
		aplicaciones_des_param_form = aplicacionContextoDesParamForm(instance=datos_api)
		aplicacion_acti_temp_param_form = aplicacionBitActTemplateParamForm(instance=datos_api)
		##Si se ha seleccionado anadir linea y se han mandado datos por POST para guardar los datos en la BD
		if request.method == 'POST':

			#pdb.set_trace()
			##Recogemos los datos del formulario
			linea_form = lineaContextoForm(request.POST)
			#Copiamos el formulario devuelto en otro,para dar valores al context, script y a la prioridad de la linea, ya que la instancia del QueryDict del request.POST es inmutable
			values_post = request.POST.copy()
			values_post.__setitem__('context',request.GET.get('context'))
			values_post.__setitem__('appdata',request.POST.get('script'))
			num_lineas = linea.objects.filter(context=request.GET.get('context'),exten=request.POST.get('exten')).count()

			#pdb.set_trace()
			##Si ya existen lineas con dicha extension en dicho contexto
			if num_lineas > 0:
				##Rebanamos los datos y nos quedamos con la linea con la prioridad mas alta
				linea_prioridad_max = linea.objects.filter(context=request.GET.get('context'),exten=request.POST.get('exten')).order_by('-priority')[0]
				##Asignamos el nuevo valor prioridad al valor del POST sumandole 1
				values_post.__setitem__('priority',linea_prioridad_max.priority+1)
			else:
			##Si no existen lineas en ese contexto de dicha extension le asignamos la prioridad 1
				values_post.__setitem__('priority',1)

			
			##Creamos un nuevo formulario de linea con los nuevos datos
			linea_form = lineaContextoForm(values_post)

			parametros_form = parametrosLineaContextoForm(request.POST)
			##Recogemos los datos del formulario de aplicaciones para obtener el nombre del script y para asignar el id_api a la nueva tupla de la tabla parametros
			api_form = aplicacionContextoForm(request.POST)
	
			 ##Comprobamos que los campos no sean nulos y sean de acuerdo al tipo definido, ademas tenemos que hacer esto antes de acceder a los datos del formulario con cleaned_data
			if linea_form.is_valid() and parametros_form.is_valid():

				#pdb.set_trace()
	##sacamos la api seleccionada segun el nombre del sript para sacar la id_api del modelo parametros
				api_sele = aplicaciones.objects.get(script=request.POST.get('script'))

	##Antes de crear la nueva tupla de parametros tenemos que crear la nueva linea
				linea_form.save()
 
			##Sacamos  nueva linea que acabamos de crear con la maxima prioridad
				linea_nueva = linea.objects.filter(context=request.GET.get('context'),exten=request.POST.get('exten')).order_by('-priority')[0]
	
 
                                ##########################################################

                                ##################TODOS LOS VALORES DE TODOS LOS PARAMETROS##########
				para1 = parametros_form.cleaned_data['param1']
				para2 = parametros_form.cleaned_data['param2']
				para3 = parametros_form.cleaned_data['param3']
				para4 = parametros_form.cleaned_data['param4']
				para5 = parametros_form.cleaned_data['param5']
				para6 = parametros_form.cleaned_data['param6']
				para7 = parametros_form.cleaned_data['param7']
				para8 = parametros_form.cleaned_data['param8']
				para9 = parametros_form.cleaned_data['param9']
				para10 = parametros_form.cleaned_data['param10']
                                ####################################################################

                                #Guardamos TODOS los datos en la base de datos y redirigimos
				nuevos_parametros = parametros(id_api=api_sele,id_linea=linea_nueva,param1=para1,param2=para2,param3=para3,param4=para4,param5=para5,param6=para6,param7=para7,param8=para8,param9=para9,param10=para10)
				
				nuevos_parametros.save()				

			return HttpResponseRedirect('/admin/dialplan/mod_contexto/?context='+contexto_sele+'&add_linea=1')
###################################################################################################################


        return render_to_response('dialplan/mod_contexto.html',{'lista_moh':lista_moh,'lista_valores_audio': lista_valor_ast,'lista_opciones_audio' : lista_opciones, 'mapa_audios' : mapa_audio ,'id_api': id_api,'lista_contextos':lista_contextos, 'nombre_api': nombre_api, 'aplicacion_des_param_form':aplicaciones_des_param_form,'aplicacion_nom_param_form':aplicacion_nom_param_form,'aplicacion_temp_param_form': aplicacion_acti_temp_param_form,'num_param':num_param,'param_form' :parametros_form, 'lista_api': lista_api, 'add_linea': add_linea ,'aplicacion_form': aplicacion_form, 'linea_form': linea_form,'linea': linea_sele,'lista_lineas' : lineas_sele, 'contexto' : contexto_sele },context_instance=RequestContext(request))





@login_required(login_url='/login')
def carga_datos_nueva_linea(request):

	linea_form = {}

	lista_api = {}

	datos_api = {}

	num_param = {}

	aplicacion_form = {}

	parametros_form = {}
        
	aplicacion_nom_param_form = {}
        
	aplicaciones_des_param_form = {}

	aplicacion_acti_temp_param_form = {}

	lista_contextos = linea.objects.values('context').distinct()

	lista_audios = ficheros_audio.objects.all()

	mapa_audio = {}
	for audio in lista_audios:
		ls1 = str(audio.fichero_audio).split('/')
		ls2 = ls1[1].split('.')

		opc = ls2[0]

		mapa_audio[str(audio.nombre)]= opc


	lista_opciones = mapa_audio.keys()
	lista_valor_ast = mapa_audio.values()

	mohs = moh.objects.all()
	lista_moh = {}
	for m in mohs:
		lista_moh[str(m.name)] = str(m.name)
	lista_moh = lista_moh.values()

	nombre_api = {}	

	if request.GET.get('add_linea') and request.GET.get('id_api'):
		
		id_api = request.GET.get('id_api')
		##Esta linea es para seleccionar el div del formualrio para anadir nueva linea en la plantilla
		add_linea = 1

		linea_form = lineaContextoForm

                ##Mostramos la lista de aplicaciones disponibles
		lista_api = aplicaciones.objects.all()

		datos_api = aplicaciones.objects.get(id=id_api)

                #Sacamos el numero de parametros de la aplicacion seleccionada por defecto
		num_param = datos_api.num_para

                #Generamos el formulario de los datos de la aplicacion de la api seleccionada por defecto
		aplicacion_form = aplicacionContextoForm(instance=datos_api)

                #Sacamos el formulario de los parametros de la aplicacion seleccionada por defecto
		parametros_form = parametrosLineaContextoForm()
                ####Sacamos los formularios con los nombres y las descripciones de la aplicacion
		aplicacion_nom_param_form = aplicacionContextoParamForm(instance=datos_api)
		aplicaciones_des_param_form = aplicacionContextoDesParamForm(instance=datos_api)
		aplicacion_acti_temp_param_form = aplicacionBitActTemplateParamForm(instance=datos_api)	
		
		nombre_api = datos_api.nombre

	return render_to_response('dialplan/add_linea.html', {'lista_moh':lista_moh,'lista_valores_audio': lista_valor_ast,'lista_opciones_audio' : lista_opciones,'mapa_audios' : mapa_audio ,'add_linea': add_linea ,'id_api': id_api,'nombre_api': nombre_api,'lista_contextos':lista_contextos, 'linea_form': linea_form, 'lista_api': lista_api, 'num_param': num_param, 'aplicacion_form': aplicacion_form,'param_form' :parametros_form, 'aplicacion_des_param_form':aplicaciones_des_param_form,'aplicacion_temp_param_form': aplicacion_acti_temp_param_form,'aplicacion_nom_param_form':aplicacion_nom_param_form }, context_instance=RequestContext(request) )


##Funcion que modifica el parametro commented de la base de datos
@login_required(login_url='/login')
def mod_linea_comentada(request):

	contexto = request.GET.get('context')
	extension = request.GET.get('exten')
	prioridad = request.GET.get('priority')

	##Devuelve el numero de filas modificadas de la tabla 
#	l1 = linea.objects.filter(context=contexto,exten=extension,priority=prioridad).update(commented=1)

	##Seleccionamos la linea y comprobamos el valor de commented
	l = linea.objects.get(context=contexto,exten=extension,priority=prioridad)
	
	if(l.commented == 1):
		linea.objects.filter(context=contexto,exten=extension,priority=prioridad).update(commented=0)
	else:
		linea.objects.filter(context=contexto,exten=extension,priority=prioridad).update(commented=1)

	##Devolvemos la funcion render_to_response de la funcion mod_contexto 
	return mod_contexto(request)	




##Funcion que borra una linea
@login_required(login_url='/login')
def borra_linea(request):

	contexto = request.GET.get('context')
	extension = request.GET.get('exten')
	prioridad = request.GET.get('priority')

	lista_api = aplicaciones.objects.all()
	lista_lineas = linea.objects.filter(context=contexto)


	num = linea.objects.filter(context=contexto,exten=extension,priority=prioridad).count()

	if(num >= 1):
		l = linea.objects.get(context=contexto,exten=extension,priority=prioridad)
		l.delete()

	return render_to_response('dialplan/lista_lineas.html',{ 'lista_api': lista_api, 'lista_lineas': lista_lineas },context_instance=RequestContext(request))

	
@login_required(login_url='/login')
def cambia_linea(request):

	id_linea_sele = request.GET.get('id_linea_sele')

	#sacamos la linea seleccionada
	linea_sele = linea.objects.get(id=id_linea_sele)
	
	##Creamos UNA lista con los id el orden de las lineas del determiando contexto
	li = list(linea.objects.filter(context=request.GET.get('context')).values_list('id',flat=True))

	#sacamos la posicion de la lista de los id de la linea seleccionada
#	pos_linea_sele = li.index(id_linea_sele) Esto da error de tipo, al index hay que pasarle
	# un valor y no una variable
	###############Para solventar esto: ####################
	pos_linea_sele = 0
	pos_linea_cam = 0
	for elem in li:
		if int(elem) == int(id_linea_sele):				
			break
		pos_linea_sele = pos_linea_sele + 1
	########################################################


	if request.GET.get('bajar')=='1' and (pos_linea_sele)<len(li):
		pos_linea_cam = pos_linea_sele+1
	else:
		pos_linea_cam = pos_linea_sele


	if request.GET.get('subir')=='1' and (pos_linea_sele)>0:
		pos_linea_cam = pos_linea_sele-1
	elif request.GET.get('bajar')=='1' and (pos_linea_sele+1)<len(li):
		pos_linea_cam = pos_linea_sele+1
	else:
		pos_linea_cam = pos_linea_sele

	#pdb.set_trace()	

	linea_cam = linea.objects.get(id=li[pos_linea_cam])

	##Intercambiamos el valor de la prioridad de las dos lineas si la extensiones en la misma
	if linea_sele.exten == linea_cam.exten:
		aux = linea_sele.priority
		linea_sele.priority = linea_cam.priority
		linea_cam.priority = aux

		linea_sele.save()
		linea_cam.save()
	
	contexto = request.GET.get('context')
	lista_api = aplicaciones.objects.all()
	lista_lineas = linea.objects.filter(context=contexto)

	return render_to_response('dialplan/lista_lineas.html',{ 'lista_api': lista_api, 'lista_lineas': lista_lineas },context_instance=RequestContext(request))





