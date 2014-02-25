# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

#Para uso de la funcion HttpResponseRedirect (redireccionar paginas)
from django.http import HttpResponseRedirect

#para conexion con bases de datos externas
import sqlite3 as dbapi

from django.conf import settings


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django.template import RequestContext

#Importamos los formularios
from forms import consulta_cdr_form

#Incluimos la funcion datetime de django
from datetime import datetime

## Crear el formulario de la vista y pasarselo a la plantila

#Herramientas de DEBUG de python####
import pdb

###USO: pdb.set_trace()
###(pdb) <pulsar n para siguiente>

###################Para genererar pdfs#############
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django.template.loader import render_to_string
from django.http import HttpResponse
import codecs
###################################################

#Funcion que realiza consultas a la base de datos /var/log/asterisk/master.db
#Para obtener el registro de llamadas

@login_required(login_url='/login/')
def cdr(request):
	usuario=request.user
                #Realizamos la conexion a la base de datos de tipo sqlite donde Asterisk va guardando los logs de todas las llamadas
        ## DOCUMENTACION ->> http://docs.python.org/2/library/sqlite3.html
	bbdd = dbapi.connect(settings.STATIC_ROOT+"api_cdr/bbdd/cdr.db")
	cursor = bbdd.cursor()
	lista_con_formato = []

	men =''
	hay_fecha_ini = 0

	genera_pdf = 0	

        #Si existen datos por POST
        #if request.method=='POST':
	if request.GET:
                #Recojo los datos en el formulario
		formulario = consulta_cdr_form(request.GET)

		genera_pdf = request.GET['genera_pdf']		

		contexto = request.GET['contexto']
		fecha_inicio = request.GET['fecha_inicio']
		fecha_fin = request.GET['fecha_fin']
		duracion_mas_de = request.GET['duracion_mas_de']
		duracion_menos_de = request.GET['duracion_menos_de']
		extension_llamante = request.GET['extension_de']
                #Herramienta muy util para DEBUG
#               pdb.set_trace()

                ##Si se ha indicado una fecha de inicia para la busqueda###
		if fecha_inicio != '':
									
	
			hay_fecha_ini = 1

			##Si no se ha indicado una fecha final para la busqueda, ponemos la fecha actual
			if fecha_fin=='':
				fecha_fin = datetime.now().strftime('%Y-%m-%d')
	
			msg_dura = ''	
			if duracion_mas_de=='':
				duracion_masde=int(0)
			else:
				duracion_masde = int(duracion_mas_de)*60
				#nhoras, nmin = divmod(long(duracion_masde),60)
                                #nseg,p = divmod(long(nmin),60)	
				msg_dura = ' con una duracion de mas de '+duracion_mas_de+' minutos'

			if duracion_menos_de=='':
				##Si nos esta definido el  numero maximo de minutos multiplicamos por 2 los segundos que tiene un dia   
                                duracion_menosde=int(86400)*2*60
                        else:
                                duracion_menosde = int(duracion_menos_de)*60
                                #nhoras, nmin = divmod(long(duracion_masde),60)
                                #nseg,p = divmod(long(nmin),60)
				if duracion_mas_de=='': 
                                	msg_dura = ' con una duracion menor de '+duracion_menos_de+' minutos'
				else:
					msg_dura = msg_dura +' y con una duracion menor de '+duracion_menos_de+' minutos'

			men = 'Llamadas registradas desde el '+formato_fecha(fecha_inicio)+' hasta el '+formato_fecha(fecha_fin)+msg_dura
			
			consulta = """select strftime('%d/%m/%Y',calldate),strftime('%H:%M',calldate),clid,dcontext,dstchannel,duration,disposition from cdr where cast(duration as integer)>=? and cast(duration as integer)<=?  and ( (julianday(calldate)>julianday(date(?))) and julianday(calldate)<julianday(date(?)) ) and dcontext in( select case when ? = '*' then dcontext else (select dcontext from cdr where dcontext=?) end  from cdr) order by calldate desc; """

			

			cursor.execute(consulta ,(duracion_masde,duracion_menosde,fecha_inicio,fecha_fin,contexto,contexto,) )

				



		else:
		###Si se pulsa sobre el boton buscar sin fecha de inicio
			##Llamadas de hoy del contexto seleccionado

			hay_fecha_ini = 0
			men = " Llamadas registradas de hoy" 
			fecha_inicio = datetime.now()
			
			consulta = """ select (strftime('%d/%m/%Y',calldate))as fecha,(strftime('%H:%M',calldate))as hora,clid,dcontext,dstchannel,duration,disposition from cdr where (julianday(calldate)>julianday(date(?))) and dcontext in( select case when ? = '*' then dcontext else (select dcontext from cdr where dcontext=?) end  from cdr) order by calldate desc ; """

			cursor.execute(consulta ,(fecha_inicio,contexto,contexto,) )


        #################Sacamos la lista de la ultima consulta ejecutada########
		lista_registros = cursor.fetchall()
		lista_con_formato = formato_lista_registros(lista_registros)	
		
		if extension_llamante!='':
			men = men + " de la extension "+extension_llamante
			lista_con_formato = formato_lista_registros_con_ext(lista_con_formato,extension_llamante)		

	else:

		contexto ='*'
		formulario = consulta_cdr_form()

		hay_fecha_ini = 1		
		men = 'Llamadas registradas de hoy'
		fecha_inicio = datetime.now()

		consulta = """ select strftime('%d-%m-%Y',calldate),strftime('%H:%M',calldate),clid,dcontext,dstchannel,duration,disposition from cdr where (julianday(calldate)>julianday(date(?))) and dcontext in( select case when ? = '*' then dcontext else (select dcontext from cdr where dcontext=?) end  from cdr) order by calldate desc; """

		cursor.execute(consulta ,(fecha_inicio,contexto,contexto,) )
		
		lista_registros = cursor.fetchall()
		lista_con_formato = formato_lista_registros(lista_registros)



	cursor.close()
	bbdd.close()

	
	if genera_pdf == '1':
		return llamadas_pdf(request,formulario,lista_con_formato,men,hay_fecha_ini)


	return render_to_response('cdr/cdr.html',{'formulario':formulario.as_p(), 'lista_registros':lista_con_formato, 'msg' : men, 'hay_fecha_ini':hay_fecha_ini },context_instance=RequestContext(request))


def formato_fecha(string_fecha):
		
	##Formato del string_fecha: '%Y-%m-%d'
	fecha_lista = string_fecha.split('-')
	anio = fecha_lista[0]
	mes = fecha_lista[1]
	dia = fecha_lista[2]

	return dia+'/'+mes+'/'+anio

def formato_lista_registros(lista_registros):

	dic = []

	##Le damos formato a la duracion de la llamada y al destino de la llamada
	for llamada in lista_registros:  
		nhoras, duracion = divmod(long(str(llamada[5])), 3600)
		nmin, nseg = divmod(duracion,60)
	
		dest = str(llamada[4]).split('-')[0]

		dic.append( (llamada[0],llamada[1],llamada[2],llamada[3],str(dest),str(nhoras).zfill(2)+':'+str(nmin).zfill(2)+':'+str(nseg).zfill(2) , llamada[6]) )

	return dic

def formato_lista_registros_con_ext(lista_registros,extension_llamante):

	dic = []
		
	for llamada in lista_registros:
		lla = str(llamada[2]).split('<')[1].split('>')[0]
		if lla == str(extension_llamante):
			dic.append((llamada[0],llamada[1],llamada[2],llamada[3],llamada[4],llamada[5],llamada[6]))

	return dic


#############################################Funciones para crear pdfs####################

def generar_pdf(html):
	# Funcion para generar el archivo PDF y devolverlo mediante HttpResponse
	#html = render_to_string('cdr/cdr.html', {'formulario':formulario.as_p(), 'lista_registros':lista_con_formato, 'msg' : men, 'hay_fecha_ini':hay_fecha_ini }, context_instance=RequestContext(request))
	
	result = StringIO.StringIO()
	pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
	#pdf = pisa.pisaDocument(StringIO.StringIO(html), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), mimetype='application/pdf')
	return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))



def llamadas_pdf(request,formulario,lista_con_formato,men,hay_fecha_ini):
	# vista de ejemplo con un hipotético modelo Libro
#	libro=get_object_or_404(Libro, id=id)
#	html = render_to_string('libro_pdf.html', {'pagesize':'A4', 'libro':libro}, context_instance=RequestContext(request))
	html = render_to_string('cdr/registro_de_llamadas.html', {'formulario':formulario.as_p(), 'lista_registros':lista_con_formato, 'msg' : men, 'hay_fecha_ini':hay_fecha_ini }, context_instance=RequestContext(request))

	return generar_pdf(html)




