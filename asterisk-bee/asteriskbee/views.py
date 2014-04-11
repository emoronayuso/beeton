from django.shortcuts import render_to_response
import datetime


#Para uso de la funcion HttpResponseRedirect (redireccionar paginas)
from django.http import HttpResponseRedirect


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django.template import RequestContext


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

def home(request):
	return HttpResponseRedirect('/login')

