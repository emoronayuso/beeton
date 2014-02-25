from django.shortcuts import render_to_response
import datetime


#Para uso de la funcion HttpResponseRedirect (redireccionar paginas)
from django.http import HttpResponseRedirect


##Importamos las vistas de las diferentes funcionalidades
#from asteriskbee.vistas_cdr import cdr

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django.template import RequestContext


#########FUNCIONES DE VISTA DE EJEMPLOS#################
def current_datetime(request):
	now=datetime.datetime.now()
	#La funcion render_to_response crea los objetos Context y HttpRequest y renderiza la plantilla, que se le pasa como primer parametro seguido de los valores del Context,
	#EN DEFINITIVA ES UN ENVOLTORIO DE LA FUNCION get_template
	#NOTA: si tenemos muchas variables para la plantilla es util usar la llama a la funcion locals() 
	#pero teniendo en cuanta su nombre que tiene que ser el mismo que el del Context
	#Ej:
	# current_date = datetime.datetime.now()
	#return render_to_response('fecha_hora/current_datetime.html', locals())
	#
	#
	#NOTA con respecto a las plantillas, podemos incluir plantillas dentro de otras con la 
	#etiqueta {% include 'nombre_plantilla' %} o {% include nombre_variable %}
	#Si la variable DEBUG = True y la plantila no se encuantra devuelve el error,
	#si esta a False no devuelve el error (no da fallo) si la plantilla no se encuentra
	return render_to_response('fecha_hora/current_datetime.html', {'current_date' : now})

def hours_ahead(request, offset):
	offset = int(offset)
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	
	#html = "<html><body> In %s hour(s), it will be %s. </body></html> " % (offset, dt)
	#return HttpResponse(html)
	return render_to_response('fecha_hora/hours_ahead.html',{'dt' : dt, 'offset' : offset})

def lee_y_muestra_sip(request):
	f = open("/etc/asterisk/sip.conf","r")
	completo = f.read()
	f.close()
	return render_to_response('lee_sip.html',{'fichero_entero' : completo})



####################################################################

def nuevo_usuario(request):
        if request.method=='POST':
                formulario = UserCreationForm(request.POST)
                if formulario.is_valid:
                        formulario.save()
                        return HttpResponseRedirect('/')
        else:
                formulario = UserCreationForm()
        return render_to_response('nuevousuario.html',{'formulario':formulario}, context_instance=RequestContext(request))



def ingresar(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/admin')
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/admin/status/')
				else:
					errores = True
					return render_to_response('ingresar.html',{'formulario':formulario,'errores': errores}, context_instance=RequestContext(request))
			else:
				errores = True
				return render_to_response('ingresar.html',{'formulario':formulario,'errores': errores}, context_instance=RequestContext(request))
	else:
		formulario = AuthenticationForm()
	return render_to_response('ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))



@login_required(login_url='/login')
def admin(request):
	usuario = request.user
	return render_to_response('admin.html',{'usuario':usuario}, context_instance=RequestContext(request))

@login_required(login_url='/login')
def cerrar(request):
	logout(request)
	return HttpResponseRedirect('/')

#@login_required(login_url='/login')
#def server_status(request):
#	usuario = request.user
#	return render_to_response('server_status/status.html', context_instance=RequestContext(request))


def home(request):
	return HttpResponseRedirect('/login')

@login_required(login_url='/login')
def consola(request):
	usuario = request.user
	return render_to_response('consola/consola.html', context_instance=RequestContext(request))




	
