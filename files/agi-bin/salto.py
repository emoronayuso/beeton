#!/usr/bin/env python2.6

####Descripcion de la funcion salto########################################################
# Salta a una determianda linea de cualquier contexto, condicional o incondicionalmente ###
##########################################################################################
####NUMERO DE PARAMETROS : X
####param1: descripcion del parametro
####  ....

## .....

###########Funcion de salto de Asterisk #####################################################
##salto incondicional a un contexto,extencion,prioridad determinada
##
## Goto(context,extension,priority)
## Goto(extension,priority)
## Goto(priority)

##GotoIf(condition?label1[[:label2])
##
## USAREMOS ESTE FORMATO DE PARA GENEREAR LAS CONDICIONES:
##    GotoIf(condition?[context1],[extension1],[priority1]:[context2],[extension2],[priority2])
##
##  Ejemplo:  exten => s,n,GotoifTime(8:00-14:00,mon-fri,*,*?abierto,s,1)
##############################################################################################

from pyst.agi import *

#importamos las funciones basicas de accesos a la base de datos
from funciones_basicas import *


##Lista de aplicaciones de asterisk http://www.voip-info.org/wiki/view/Asterisk+-+documentation+of+application+commands

def salto():

	##Lo primero sera sacar el contexto, la extension del receptor de la llamada y
	## la prioridad para sacar la id de la linea del dialplan
	## para ello accedemos a las variables de entorno: agi_context, agi_extension, agi_priority 

	
	miagi = AGI()
	miagi.verbose("--------------La llamada realiza un salto--------------")
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

		cad = "Se genera un salto desde el contexto ->"+miagi.env['agi_context']+" hacia el contexto ->"+str(lista[0])+ "con la extension ->"+str(lista[1])+" y prioridad->"+str(lista[2])

		#miagi.verbose("Llamada desde----> %s" % callerId )
		miagi.verbose("%s" % cad)
		#### El parametro de segundo de la espera
		opcion_salto = str(lista[0])+","+str(lista[1])+","+str(lista[2])
		#miagi.verbose("-------->  %s " % opcion_dial)
		#miagi.answer()
		#miagi.stream_file('demo-congrats')
		#miagi.appexec('noop',"Llamada desde %s opciones -> %s" % callerId,opcion_dial)
		#miagi.noop()
		miagi.appexec('Goto', opcion_salto)
		miagi.verbose("-----------------------------------------------------------")
		#miagi.hangup()

if __name__ == "__main__":
	salto()
