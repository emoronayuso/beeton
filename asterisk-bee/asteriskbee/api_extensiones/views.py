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
from django.conf import settings

#Incluimos el modelo para poder crear los formularios
from models import * 
from asteriskbee.api_dialplan.models import *

#Para modificar una extension
#from django.forms.models import modelformset_factory

#Herramientas de DEBUG de python####
import pdb

###USO: pdb.set_trace()
###(pdb) <pulsar n para siguiente>

#Funcion que muestra la lista de las extensiones sip
@login_required(login_url='/login')
def ext_sip(request):
	#lista = sip.objects.filter(username='125')
	#lista_ext = sip.objects.all()

	lista_ext = sip.objects.values('id','callerid')
	
	#Creamos un diccionario para gestionar las extensiones
	# (key,valor) = (id,"Nombre y Apellidos <ext>")
	mapa = {}
	for ext in lista_ext:
		mapa[ext['id']] = ext['callerid']	
		
        return render_to_response('extensiones/sip/sip.html',{'mapa_extensiones_sip' : mapa },context_instance=RequestContext(request))



@login_required(login_url='/login')
def add_sip(request):
        #usuario = request.user
	
	num_ext = 0
	pass_ok = True

	if request.method == 'POST':

		sip_form_user_per = sipUserFormPer(request.POST)
		sip_form_user_aco = sipUserFormAco(request.POST)
                sip_form_option  =  sipOptionForm(request.POST)
		confir_pass_form = ConfirPassForm(request.POST)

		
		
		##Comprobamos que los campos no sean nulos y sean de acuerdo al tipo definido, y que no haya dos usuarios con la misma extension, y que la confirmacion de clave sea correcta
		num_ext = sip.objects.filter(username=request.POST.get('username')).count()
		pass_ok = (request.POST.get('secret') == request.POST.get('confirma') )		

		if sip_form_user_per.is_valid() and sip_form_option.is_valid() and sip_form_user_aco.is_valid() and confir_pass_form.is_valid() and (num_ext==0) and pass_ok:
			#Si los datos del formulario son validos, le damos valor al callerid
			nom = request.POST.get('nombre')
			ape = request.POST.get('apellidos')
			ext = request.POST.get('username')

			#pdb.set_trace()
			# Construimos la cadena formato del callerid	
			ca = '"' + nom + " " + ape + '"' + ' <'+ ext +'>'
			
			#Copiamos el formulario devuelto en otro,para dar un valor al callerid 
                        #, ya que la instancia del QueryDict del request.POST es inmutable
                        #post_values = request.POST.copy() 
			values_post = request.POST.copy()	
			values_post.__setitem__('callerid',ca)


			##REGLAS DE VALIDACION DEFINIDAS  -> No funciona mirar
			#confirma = confir_pass_form.clean_data['confirma']			

			#Guardamos TODOS los datos en la base de datos y creamos
			# dos nuevas liens en el plan de llamadas del contexto usuarios
			# 1 - espera (2 segundos), 2- Responder llamadas 
			sip_form = sipForm(values_post)
			if sip_form.is_valid():
				sip_form.save()
				
				l = linea(context='usuarios',exten=ext,priority=1,app='AGI',appdata='esperar.py')
				l.save()
				api_sele = aplicaciones.objects.get(script='esperar.py')
				param = parametros(id_api=api_sele,id_linea=l,param1='2')
				param.save()
				
				l = linea(context='usuarios',exten=ext,priority=2,app='AGI',appdata='responder_llamada.py')
				l.save()
				api_sele = aplicaciones.objects.get(script='responder_llamada.py')
				param = parametros(id_api=api_sele,id_linea=l)
				param.save()


			return HttpResponseRedirect('/admin/sip/')
	else:		
		sip_form_user_per = sipUserFormPer
		sip_form_user_aco = sipUserFormAco
		confir_pass_form = ConfirPassForm
		sip_form_option  =  sipOptionForm
	return render_to_response('extensiones/sip/crear_ext_sip.html',{'formulario_sip_user_per' : sip_form_user_per,'formulario_sip_user_aco':sip_form_user_aco,'formulario_confi_pass':confir_pass_form , 'formulario_sip_option' : sip_form_option, 'usuario_existe' : num_ext, 'pass_ok': pass_ok },context_instance=RequestContext(request))


#Funcion para modificar extensiones SIP
@login_required(login_url='/login')
def mod_sip(request):

	mod_sip = 1
	pass_ok = True

	sip_sele = sip.objects.get(id=request.GET.get('id'))

	secret = sip_sele.secret
	username = sip_sele.username
	
	if request.method == 'POST':

		sip_form_user_per = sipUserFormPer(request.POST)
		sip_form_user_aco = sipUserFormAco(request.POST)
		sip_form_option  =  sipOptionForm(request.POST)
		confir_pass_form = ConfirPassForm(request.POST)

		#Coprobamos que los datos sean validos y que las dos password coincidan
		pass_ok = (request.POST.get('secret') == request.POST.get('confirma') )	

		if sip_form_user_per.is_valid() and sip_form_option.is_valid() and sip_form_user_aco.is_valid() and confir_pass_form.is_valid() and pass_ok:
                        #Si los datos del formulario son validos, le damos valor al callerid
			nom = request.POST.get('nombre')
			ape = request.POST.get('apellidos')
			ext = request.POST.get('username')

                        #pdb.set_trace()
                        # Construimos la cadena formato del callerid    
			ca = '"' + nom + " " + ape + '"' + ' <'+ ext +'>'

                        #Copiamos el formulario devuelto en otro,para dar un valor al callerid 
                        #, ya que la instancia del QueryDict del request.POST es inmutable
                        #post_values = request.POST.copy() 
			values_post = request.POST.copy()
			values_post.__setitem__('callerid',ca)

			sip_a_mod = sip.objects.get(username=request.POST.get('username'))
			sip_form = sipForm(values_post, instance=sip_a_mod)
			if sip_form.is_valid():
				sip_form.save()

			return HttpResponseRedirect('/admin/sip/')
	else:  
		#Creamos el formulario relleno desde un instancia de una extension en concreto
                #datos = sip.objects.values('nombre','apellidos','name').filter(id=request.GET.get('id'))
		datos = sip.objects.get(pk=request.GET.get('id'))
		

		sip_form_user_per = sipUserFormPer(instance=datos)
		sip_form_user_aco = sipUserFormAco(instance=datos)
		confir_pass_form = ConfirPassForm
		sip_form_option  =  sipOptionForm(instance=datos)
	
	return render_to_response('extensiones/sip/mod_ext_sip.html',{'formulario_sip_user_per' : sip_form_user_per,'formulario_sip_user_aco':sip_form_user_aco,'formulario_confi_pass':confir_pass_form , 'formulario_sip_option' : sip_form_option, 'secret': secret, 'username': username, 'mod_sip':mod_sip, 'pass_ok': pass_ok },context_instance=RequestContext(request))

@login_required(login_url='/login')
def del_sip(request):

	if request.method == 'GET':
		##Eliminamos la extension y TODAS las lineas del dialplan asociadas a esta
		sip_sele = sip.objects.get(id=request.GET.get('id'))

		l = linea.objects.filter(exten=sip_sele.name)
		sip_sele.delete()
		l.delete()


	lista_ext = sip.objects.values('id','callerid')

        #Creamos un diccionario para gestionar las extensiones
        # (key,valor) = (id,"Nombre y Apellidos <ext>")
	mapa = {}
	for ext in lista_ext:
		mapa[ext['id']] = ext['callerid']

	return render_to_response('extensiones/sip/lista_ext_sip.html',{'mapa_extensiones_sip' : mapa },context_instance=RequestContext(request))
	


#############################################################################################################
###############################################EXTENSIONES IAX ##############################################
############################################################################################################

#Funcion que muestra la lista de las extensiones iax
@login_required(login_url='/login')
def ext_iax(request):
        #lista = sip.objects.filter(username='125')
        #lista_ext = sip.objects.all()

	lista_ext = iax.objects.values('name','callerid')

        #Creamos un diccionario para gestionar las extensiones
        # (key,valor) = (id,"Nombre y Apellidos <ext>")
	mapa = {}
	for ext in lista_ext:
		mapa[ext['name']] = ext['callerid']

	return render_to_response('extensiones/iax/iax.html',{'mapa_extensiones_iax' : mapa },context_instance=RequestContext(request))



@login_required(login_url='/login')
def add_iax(request):
        #usuario = request.user

	num_ext = 0
	pass_ok = True

	if request.method == 'POST':

		iax_form_user_per = iaxUserFormPer(request.POST)
		iax_form_user_aco = iaxUserFormAco(request.POST)
		iax_form_option  =  iaxOptionForm(request.POST)
		confir_pass_form = ConfirPassForm(request.POST)



                ##Comprobamos que los campos no sean nulos y sean de acuerdo al tipo definido, y que no haya dos usuarios con la misma extension, y que la confirmacion de clave sea correcta
		num_ext = iax.objects.filter(username=request.POST.get('username')).count()
		pass_ok = (request.POST.get('secret') == request.POST.get('confirma') )

		if iax_form_user_per.is_valid() and iax_form_option.is_valid() and iax_form_user_aco.is_valid() and confir_pass_form.is_valid() and (num_ext==0) and pass_ok:
                        #Si los datos del formulario son validos, le damos valor al callerid
			nom = request.POST.get('nombre')
			ape = request.POST.get('apellidos')
			ext = request.POST.get('username')
 #pdb.set_trace()
                        # Construimos la cadena formato del callerid    
			ca = '"' + nom + " " + ape + '"' + ' <'+ ext +'>'

                        #Copiamos el formulario devuelto en otro,para dar un valor al callerid 
                        #, ya que la instancia del QueryDict del request.POST es inmutable
                        #post_values = request.POST.copy() 
			values_post = request.POST.copy()
			values_post.__setitem__('callerid',ca)


                        ##REGLAS DE VALIDACION DEFINIDAS  -> No funciona mirar
                        #confirma = confir_pass_form.clean_data['confirma']                     

                        #Guardamos TODOS los datos en la base de datos
			iax_form = iaxForm(values_post)
			if iax_form.is_valid():
				iax_form.save()

				l = linea(context='usuarios',exten=ext,priority=1,app='AGI',appdata='esperar.py')
				l.save()
				api_sele = aplicaciones.objects.get(script='esperar.py')
				param = parametros(id_api=api_sele,id_linea=l,param1='2')
				param.save()

				l = linea(context='usuarios',exten=ext,priority=2,app='AGI',appdata='responder_llamada.py')
				l.save()
				api_sele = aplicaciones.objects.get(script='responder_llamada.py')
				param = parametros(id_api=api_sele,id_linea=l)
				param.save()


				return HttpResponseRedirect('/admin/iax/')
	else:  
		iax_form_user_per = iaxUserFormPer
		iax_form_user_aco = iaxUserFormAco
		confir_pass_form = ConfirPassForm
		iax_form_option  =  iaxOptionForm
	return render_to_response('extensiones/iax/crear_ext_iax.html',{'formulario_iax_user_per' : iax_form_user_per,'formulario_iax_user_aco':iax_form_user_aco,'formulario_confi_pass':confir_pass_form , 'formulario_iax_option' : iax_form_option, 'usuario_existe' : num_ext, 'pass_ok': pass_ok },context_instance=RequestContext(request))


#Funcion para modificar extensiones SIP
@login_required(login_url='/login')
def mod_iax(request):

	mod_iax = 1
	pass_ok = True

	iax_sele = iax.objects.get(name=request.GET.get('name'))

	secret = iax_sele.secret
	username = iax_sele.username

	if request.method == 'POST':

		iax_a_mod = iax.objects.get(name=request.POST.get('name'))

		iax_form_user_per = iaxUserFormPer(request.POST, instance=iax_a_mod)
		iax_form_user_aco = iaxUserFormAco(request.POST, instance=iax_a_mod)
		iax_form_option  =  iaxOptionForm(request.POST, instance=iax_a_mod)
		confir_pass_form = ConfirPassForm(request.POST)

                #Coprobamos que los datos sean validos y que las dos password coincidan
		pass_ok = (request.POST.get('secret') == request.POST.get('confirma') )

		if iax_form_user_per.is_valid() and iax_form_option.is_valid() and iax_form_user_aco.is_valid() and confir_pass_form.is_valid() and pass_ok:
                        #Si los datos del formulario son validos, le damos valor al callerid
			nom = request.POST.get('nombre')
			ape = request.POST.get('apellidos')
			ext = request.POST.get('username')

                        #pdb.set_trace()
                        # Construimos la cadena formato del callerid    
			ca = '"' + nom + " " + ape + '"' + ' <'+ ext +'>'

                        #Copiamos el formulario devuelto en otro,para dar un valor al callerid 
                        #, ya que la instancia del QueryDict del request.POST es inmutable
                        #post_values = request.POST.copy() 
			values_post = request.POST.copy()
			values_post.__setitem__('callerid',ca)

			#iax_a_mod = iax.objects.get(name=request.POST.get('name'))
			iax_form = iaxForm(values_post, instance=iax_a_mod)
			if iax_form.is_valid():
				iax_form.save()

			return HttpResponseRedirect('/admin/iax/')

	else:
                #Creamos el formulario relleno desde un instancia de una extension en concreto
                #datos = sip.objects.values('nombre','apellidos','name').filter(id=request.GET.get('id'))
		datos = iax.objects.get(pk=request.GET.get('name'))


		iax_form_user_per = iaxUserFormPer(instance=datos)
		iax_form_user_aco = iaxUserFormAco(instance=datos)
		confir_pass_form = ConfirPassForm
		iax_form_option  =  iaxOptionForm(instance=datos)

	return render_to_response('extensiones/iax/mod_ext_iax.html',{'formulario_iax_user_per' : iax_form_user_per,'formulario_iax_user_aco':iax_form_user_aco,'formulario_confi_pass':confir_pass_form , 'formulario_iax_option' : iax_form_option, 'secret': secret, 'username': username, 'mod_iax':mod_iax, 'pass_ok': pass_ok },context_instance=RequestContext(request))



@login_required(login_url='/login')
def del_iax(request):

	if request.method == 'GET':
		iax_sele = iax.objects.get(name=request.GET.get('name'))
		##Eliminamos la extensions y TODAS las lineas del dialplan asociadas
		iax_sele.delete()
		
		l = linea.objects.filter(exten=request.GET.get('name'))
		l.delete()



	lista_ext = iax.objects.values('name','callerid')

        #Creamos un diccionario para gestionar las extensiones
        # (key,valor) = (id,"Nombre y Apellidos <ext>")
	mapa = {}
	for ext in lista_ext:
		mapa[ext['name']] = ext['callerid']

	return render_to_response('extensiones/iax/lista_ext_iax.html',{'mapa_extensiones_iax' : mapa },context_instance=RequestContext(request))


