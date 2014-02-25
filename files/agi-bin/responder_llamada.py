#!/usr/bin/env python2.6

from pyst.agi import *
import sys

#importamos las funciones basicas de accesos a la base de datos
from funciones_basicas import *

def responder_llamada():

	miagi = AGI()

	###Sacamos el id de la linea
	id_linea = get_id_linea(miagi.env['agi_context'],miagi.env['agi_extension'],miagi.env['agi_priority'])

	##Comprobamos antes que la linea NO este comentada
	if get_commented_linea(id_linea) == '0':

		miagi.verbose("--------------Llamada utilizando AGI en python--------------")
		ext_dest = miagi.env['agi_extension']
		callerId = miagi.env['agi_callerid']
		cad = "---->Llamada desde--->"+callerId+" hacia--->"+ext_dest
		miagi.verbose("%s" % cad)
		tipo_dest = get_tipo_exten(ext_dest)
		
		###Ver todos los parametroes de la api DIAL
		##http://www.voip-info.org/wiki/view/Asterisk+cmd+Dial

		opcion_dial = str(tipo_dest) + '/' + ext_dest + ',90,m,r'
		miagi.verbose("La opcion dial es -------->  %s " % opcion_dial)
		miagi.answer()


		##Para evitar que el script termine al terminar la llamada a la aplicacion Dial####
		miagi.set_variable('AGISIGHUP','no')                                             ## 
		###################################################################################		

		miagi.appexec('dial', opcion_dial)

		miagi.set_variable('AGISIGHUP','yes')

		siguiente_prio = int(miagi.env['agi_priority'])+1
		miagi.goto_on_exit(miagi.env['agi_context'],ext_dest,str(siguiente_prio))

		miagi.verbose("-----------------------------------------------------------")
	
	else:
		cad = "ESTA COMENTADA! - La linea de responder llamadas del contexto->"+miagi.env['agi_context']+ " de la extencion->"+miagi.env['agi_extension']+" y prioridad->"+miagi.env['agi_priority']

		miagi.verbose("%s" % cad)


if __name__ == "__main__":
	responder_llamada()
