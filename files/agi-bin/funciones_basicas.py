#!/usr/bin/env python2.6

#para conexion con bases de datos externas
import sqlite3 as dbapi


def get_id_linea(context,exten,priority):

	## DOCUMENTACION ->> http://docs.python.org/2/library/sqlite3.html

	bbdd = dbapi.connect("/home/asterisk-bee/db_asteriskbee_sqlite.db")

	cursor = bbdd.cursor()
	lista_registros = []

	consulta = """ select id from api_dialplan_linea where context=? and exten=? and priority=?; """

	cursor.execute(consulta ,(context,exten,priority,) )

	lista_registros = cursor.fetchone()

	cursor.close()
	bbdd.close()

	return str(lista_registros[0])


def get_num_param(id_linea):

	bbdd = dbapi.connect("/home/asterisk-bee/db_asteriskbee_sqlite.db")

	cursor = bbdd.cursor()
	lista_registros = []

	consulta = """ select num_para from api_dialplan_aplicaciones where id=(select id_api from api_dialplan_parametros where id_linea=?); """

	cursor.execute(consulta ,(id_linea,) )

	lista_registros = cursor.fetchone()

	cursor.close()
	bbdd.close()

	return str(lista_registros[0])

def get_lista_param(id_linea):

	bbdd = dbapi.connect("/home/asterisk-bee/db_asteriskbee_sqlite.db")

	cursor = bbdd.cursor()
	lista_registros = []

	consulta = """ select param1,param2,param3,param4,param5,param6,param7,param8,param9,param10 from api_dialplan_parametros where id_linea=?; """

	cursor.execute(consulta ,(id_linea,) )

	lista_registros = cursor.fetchone()

	cursor.close()
	bbdd.close()

	return lista_registros

##Devuelve el valor que indica si la linea esta comentada [1] o no [0]
def get_commented_linea(id_linea):

        ## DOCUMENTACION ->> http://docs.python.org/2/library/sqlite3.html

        bbdd = dbapi.connect("/home/asterisk-bee/db_asteriskbee_sqlite.db")

        cursor = bbdd.cursor()
        lista_registros = []

        consulta = """ select commented from api_dialplan_linea where id=?; """

        cursor.execute(consulta ,(id_linea,) )

        lista_registros = cursor.fetchone()

        cursor.close()
        bbdd.close()  

        return str(lista_registros[0])

def get_tipo_exten(exten):

	tipo=''
	
	bbdd = dbapi.connect("/home/asterisk-bee/db_asteriskbee_sqlite.db")

	cursor = bbdd.cursor()
	lista_registros = []
	
	consulta = """ select count(*) from api_extensiones_sip where username=?; """

	cursor.execute(consulta ,(exten,) )

	lista_registros = cursor.fetchone()

	if int(lista_registros[0]) == 1:
		tipo='SIP'
	else:
		consulta = """ select count(*) from api_extensiones_iax where username=?; """
		cursor.execute(consulta ,(exten,) )
		lista_registros = cursor.fetchone()

		if int(lista_registros[0]) == 1:
			tipo='IAX2'

	cursor.close()
	bbdd.close()

	return tipo


	
	
