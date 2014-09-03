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

#Herramientas de DEBUG de python####
import pdb

###USO: pdb.set_trace()
###(pdb) <pulsar n para siguiente>


#libreria del sistema para ejecutar comandos
import os

########################################################################
##Esto es importante importarlo antes de matplotlib.pyplot para        #
## que no se use ningun backend de X Windows y generar graficas en 2D  #
import matplotlib						       #
matplotlib.use('Agg')						       #	
########################################################################

import matplotlib.pyplot as plt
import numpy as np
import calendar
from datetime import datetime

import sqlite3 as dbapi

from asteriskbee.api_extensiones.models import sip,iax

@login_required(login_url='/login')
def server_status(request):
	usuario = request.user

	### STATIC_ROOT = '/var/www/asterisk-bee/asteriskbee/'

	#####################################CARGA CPU#####################################
	os.system("top -n 1 > "+settings.STATIC_ROOT+"api_status/archivos/fich_out_carga_cpu; sed -i '1,7d' "+settings.STATIC_ROOT+"api_status/archivos/fich_out_carga_cpu; cat "+settings.STATIC_ROOT+"api_status/archivos/fich_out_carga_cpu | tr ' ' '-' | tr -s '-' | cut -d '-' -f 10 | tr ',' '.' > "+settings.STATIC_ROOT+"api_status/archivos/fich_out_carga_cpu2")

	total = 0.0

	f = open(settings.STATIC_ROOT+"api_status/archivos/fich_out_carga_cpu2",'r')

	while True:
		linea = f.readline()
		if not linea or float(linea)==0.0:
			break
		else:
			total = total + float(linea)

	f.close()

	carga_cpu = total
	####################################################################################

	####################################USO DE RAM ####################################
	salida = os.system('free -m | grep Mem: | tr " " "," | cut -d "," -f 20 >'+settings.STATIC_ROOT+'api_status/archivos/fich_out_uso_ram')
	f = open(settings.STATIC_ROOT+'api_status/archivos/fich_out_uso_ram','r')
	linea = f.readline().strip()
	salida = os.system('free -m | grep Mem: | tr " " "," | cut -d "," -f 12 >'+settings.STATIC_ROOT+'api_status/archivos/fich_out_ram_total')
	f2 = open(settings.STATIC_ROOT+'api_status/archivos/fich_out_ram_total','r')
	linea2 = f2.readline().strip()
        if linea == "" or linea2 == "":
            res = 50
        else:
            res =  int( ( int(linea)*100 ) / int(linea2) )
	f.close()
	f2.close()
	
	uso_ram = res
	#################################################################################

	#####################################USO_SIST_RAIZ##############################

	#os.system('df -h | grep rootfs | tr " " "," | cut -d "," -f 26 | cut -d "%" -f 1 >'+settings.STATIC_ROOT+'api_status/archivos/fich_out_uso_raiz')
	
	# df --total -h | grep ^total | tr " " "\n" | grep %$ | cut -d "%" -f 1
	os.system('df --total -h | grep ^total | tr " " "\n" | grep %$ | cut -d "%" -f 1 >'+settings.STATIC_ROOT+'api_status/archivos/fich_out_uso_raiz')

	f = open(settings.STATIC_ROOT+'api_status/archivos/fich_out_uso_raiz','r')
	linea = f.readline().strip()

	if linea == "":
		res = 0
	else:
		res = int(linea)

	f.close()
	
	uso_sist_raiz = res
  	###############################################################################

	##########################EXT REGISTRADAS #####################################

	lista_ext_sip_reg = sip.objects.exclude(ipaddr='').exclude(regseconds=0)
        lista_ext_iax_reg = iax.objects.exclude(ipaddr='').exclude(regseconds=0)

	###############################################################################	


	return render_to_response('server_status/status.html',{'lista_ext_sip_registradas' : lista_ext_sip_reg, 'lista_ext_iax_registradas' : lista_ext_iax_reg, 'por_carga_cpu' : carga_cpu, 'por_uso_ram' : uso_ram, 'por_uso_sist_raiz' : uso_sist_raiz},context_instance=RequestContext(request))


#Esta funcion nos devuelve el porcentaje de la carga media del ultimo minuto de la cpu,
#para ello hacemos uso del comando uptime
def carga_cpu(request):
#	salida = os.system("uptime | awk -F 'load average' '{print $2}' | tr ':' ' ' | cut -d ',' -f 2 >"+settings.STATIC_ROOT+'api_status/archivos/fich_out_cmd')
#	f = open(settings.STATIC_ROOT+'api_status/archivos/fich_out_cmd','r')
#	linea = f.readline().strip()


	os.system("top -n 1 > "+settings.STATIC_ROOT+"api_status/archivos/fich_out_carga_cpu; sed -i '1,7d' "+settings.STATIC_ROOT+"api_status/archivos/fich_out_carga_cpu; cat "+settings.STATIC_ROOT+"api_status/archivos/fich_out_carga_cpu | tr ' ' '-' | tr -s '-' | cut -d '-' -f 10 | tr ',' '.' > "+settings.STATIC_ROOT+"api_status/archivos/fich_out_carga_cpu2")


        total = 0.0

        f = open(settings.STATIC_ROOT+"api_status/archivos/fich_out_carga_cpu2",'r')

        while True:
                linea = f.readline()
                if not linea or float(linea)==0.0:
                        break
                else:
                        total = total + float(linea)





	f.close()

	res = total
#	if linea == '':
#		res = 0.0
#	else:
#		res = float(linea)*100
	#pdb.set_trace()
	return render_to_response('server_status/carga_cpu.html', {'por_carga_cpu' : res}, context_instance=RequestContext(request) )


def uso_ram(request):
	salida = os.system('free -m | grep Mem: | tr " " "," | cut -d "," -f 20 >'+settings.STATIC_ROOT+'api_status/archivos/fich_out_uso_ram')
	f = open(settings.STATIC_ROOT+'api_status/archivos/fich_out_uso_ram','r')
	linea = f.readline().strip()
        salida = os.system('free -m | grep Mem: | tr " " "," | cut -d "," -f 12 >'+settings.STATIC_ROOT+'api_status/archivos/fich_out_ram_total')
	f2 = open(settings.STATIC_ROOT+'api_status/archivos/fich_out_ram_total','r')
	linea2 = f2.readline().strip()
        if linea == "" or linea2 == "":
            res = 0
        else:
            res =  int( ( int(linea)*100 ) / int(linea2) ) 
	f.close()
	f2.close()
	return render_to_response('server_status/uso_ram.html', {'por_uso_ram' : res}, context_instance=RequestContext(request) )


def uso_sist_fich_raiz(request):
	os.system('df -h | grep rootfs | tr " " "," | cut -d "," -f 26 | cut -d "%" -f 1 >'+settings.STATIC_ROOT+'api_status/archivos/fich_out_uso_raiz')
	f = open(settings.STATIC_ROOT+'api_status/archivos/fich_out_uso_raiz','r')
	linea = f.readline().strip()

	if linea == "":
		res = 0
	else: 
		res = int(linea)

	f.close()
	
	return render_to_response('server_status/uso_sist_raiz.html', {'por_uso_sist_raiz' : res}, context_instance=RequestContext(request) )	


def llamadas_activas(request):

	os.system("asterisk -x 'core show channels' | grep channel | cut -d ' ' -f 1 >"+settings.STATIC_ROOT+'api_status/archivos/fich_out_canales_activos')

	f1 = open(settings.STATIC_ROOT+'api_status/archivos/fich_out_canales_activos','r')
	
	linea1 = f1.readline()
        if linea1 == "":
            canales = 0
        else:
            canales = int (linea1)

	f1.close()

	os.system("asterisk -x 'core show channels' | grep active | grep -v channels | cut -d ' ' -f 1 >"+settings.STATIC_ROOT+'api_status/archivos/fich_out_llamadas_activas')

        f2 = open(settings.STATIC_ROOT+'api_status/archivos/fich_out_llamadas_activas','r')

        linea2 = f2.readline()
        if linea2 == "":
            llamadas = 0
        else:
            llamadas = int (linea2)

        f1.close()


	return render_to_response('server_status/llamadas_activas.html', {'num_llamadas_activas' : llamadas, 'num_canales_activos': canales}, context_instance=RequestContext(request) )


def lista_extensiones_reg(request):

	lista_ext_sip_reg = sip.objects.exclude(ipaddr='').exclude(regseconds=0)
	lista_ext_iax_reg = iax.objects.exclude(ipaddr='').exclude(regseconds=0)

	return render_to_response('server_status/lista_ext_registradas.html', {'lista_ext_sip_registradas' : lista_ext_sip_reg, 'lista_ext_iax_registradas' : lista_ext_iax_reg }, context_instance=RequestContext(request) )


###### APAGAR LA PLACA ALIX ##################
@login_required(login_url='/login')          #
def shutdown(request):                       #
	os.system("shutdown -h now ")        #
###############################################





########################################################GRAFICAS########################

def grafica_uso_cpu_dia(request):

	#os.system("rm /home/asterisk-bee/asteriskbee/templates/images/temp_graficas/grafica_uso_cpu_dia.png")

	datos = {}
	### STATIC_ROOT = '/var/www/asterisk-bee/asteriskbee/'
	directorio = settings.STATIC_ROOT+"api_status/"


	#Conexion con la base de datos de estadisticas
	bbdd = dbapi.connect(directorio+"bbdd/estadisticas.db")
	cursor = bbdd.cursor()
	
	sele_valores = "select valor from api_status_marcas_graficas where tipo='cpu_dia' order by fecha_hora ;"
	cursor.execute(sele_valores)
	lista_valores = cursor.fetchall()

	sele_horas = "select strftime('%H:%M',fecha_hora) from api_status_marcas_graficas where tipo='cpu_dia' order by fecha_hora ;"
	cursor.execute(sele_horas)
	lista_de_listas_de_horas = cursor.fetchall()
	
	lista_horas = []
	for hora in lista_de_listas_de_horas:
		lista_horas.append(hora[0])


	##Cerramos la conexion con la BBDD
	cursor.close()
	bbdd.close()
	
	if len(lista_horas) == 20:
		y= lista_valores

		x= range(0,20)

		matplotlib.pyplot.ioff()

		plt.plot(x,y, color = 'green')

		plt.xticks( np.arange(20), lista_horas, rotation=45 )
		
		#plt.yticks(np.arange(100), range(0,100,10), rotation=0)
		
		plt.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
		plt.legend()  # Colocamos la leyenda
		plt.title('Carga media de la CPU')  # Colocamos el titulo del grafico
		#plt.xlabel('Tiempo')  # Colocamos la etiqueta en el eje x
		plt.ylabel('Porcentaje uso de CPU')  # Colocamos la etiqueta en el eje y

	#	open(settings.STATIC_ROOT+'templates/images/temp_graficas/grafica_uso_cpu_dia.png','r')

	#	os.system("rm /home/asterisk-bee/asteriskbee/templates/images/temp_graficas/grafica_uso_cpu_dia.png")	
	
		## STATIC_ROOT = '/var/www/asterisk-bee/asteriskbee/'
		plt.savefig(settings.STATIC_ROOT+"templates/images/temp_graficas/grafica_uso_cpu_dia.png")

		
		plt.cla()
		plt.clf()
		plt.close()

	return render_to_response('server_status/grafica_uso_cpu_dia.html', {'datos' : datos}, context_instance=RequestContext(request) )

