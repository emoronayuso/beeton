#!/usr/bin/env python2.6

####Descripcion de la funcion espera###################
# Hace esperar un numero determinado de segundos cuando se realiza la llamada a la extension###
#
####NUMERO DE PARAMETROS : 1
####param1: numero en segundos de la espera

from pyst.agi import *

#importamos las funciones basicas de accesos a la base de datos
from funciones_basicas import *


##Lista de aplicaciones de asterisk http://www.voip-info.org/wiki/view/Asterisk+-+documentation+of+application+commands

def esperar():

	##Lo primero sera sacar el contexto, la extension del receptor de la llamada y
	## la prioridad para sacar la id de la linea del dialplan
	## para ello accedemos a las variables de entorno: agi_context, agi_extension, agi_priority 

	
	miagi = AGI()
	miagi.verbose("--------------Espera unos segundos utilizando AGI en python--------------")
	ext_dest = miagi.env['agi_extension']
        tipo_ext_dest = miagi.env['agi_type']
	callerId = miagi.env['agi_callerid']

	###Sacamos el id de la linea
	id_linea = get_id_linea(miagi.env['agi_context'],miagi.env['agi_extension'],miagi.env['agi_priority'])

	##Comprobamos antes que la linea NO este comentada
	if get_commented_linea(id_linea) == '0':

		##probamos sacar el numero de parametros
		num_para = get_num_param(id_linea)

		####lista_de_parametros, en este caso solo uno param1 que hace 
                #### referencia al numero de segundos de espera
		lista = get_lista_param(id_linea)


#		cad = "La extension llamante "+tipo_ext_dest+"/"+callerId+" tiene que esperar X segundos al llamar a la extension destino "+ext_dest + "WEEEEEE---->>>>>"+ miagi.env['agi_context']+"--"+miagi.env['agi_extension']+"--"+miagi.env['agi_priority']+"--IDLINEA--->"+id_linea+"-----NUM PARAMETROS-----"+num_para+"--pepeeeL-->"+lista[0]
		cad = "La extension llamante "+tipo_ext_dest+"/"+callerId+" tiene que esperar "+str(lista[0])+" segundos al llamar a la extension destino "+ext_dest

		#miagi.verbose("Llamada desde----> %s" % callerId )
		miagi.verbose("%s" % cad)
		#### El parametro de segundo de la espera
		opcion_wait = str(lista[0])
		#miagi.verbose("-------->  %s " % opcion_dial)
		#miagi.answer()
		#miagi.stream_file('demo-congrats')
		#miagi.appexec('noop',"Llamada desde %s opciones -> %s" % callerId,opcion_dial)
		#miagi.noop()
		miagi.appexec('Wait', opcion_wait)
		miagi.verbose("-----------------------------------------------------------")
		#miagi.hangup()

	else:
		cad = "ESTA COMENTADA! - La linea de espera del contexto->"+miagi.env['agi_context']+ " de la extencion->"+ext_dest+" y prioridad->"+miagi.env['agi_priority']

		miagi.verbose("%s" % cad)
		

if __name__ == "__main__":
	esperar()
