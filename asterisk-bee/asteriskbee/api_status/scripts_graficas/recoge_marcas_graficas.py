#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
#import calendar
from datetime import datetime

from django.conf import settings
settings.configure()
import os

#para conexion con la bases de datos de beeton (asteriskbee)
import sqlite3 as dbapi

##Directorio de la aplicaion
### STATIC_ROOT = '/var/www/asterisk-bee/asteriskbee/'
#directorio = settings.STATIC_ROOT+"api_status/"
directorio = "/var/www/asterisk-bee/asteriskbee/api_status/"


##Numero de tuplas maximas por grafica
num_cpu_dia = 20


def recoge_marcas():

	#Conexion con la base de datos de estadisticas
	bbdd = dbapi.connect(directorio+"bbdd/estadisticas.db")
	cursor = bbdd.cursor()


	os.system("ps -e -o pcpu,cpu,nice,state,cputime,args --sort pcpu | sed '/^ 0.0 /d' > "+directorio+"scripts_graficas/temp/temp_cpu_dia; cat "+directorio+"scripts_graficas/temp/temp_cpu_dia | sed 's/^[ \t]*//;s/[ \t]*$//' | grep -v 'recoge_marcas_graficas.py' | cut -d ' ' -f 1 > "+directorio+"scripts_graficas/temp/temp_cpu_dia2")


	total = 0.0
	
	f = open(directorio+'scripts_graficas/temp/temp_cpu_dia2','r')

	##Leemos la primera linea para quitar el encabezado
	linea = f.readline()

	while True:
		linea = f.readline()
		if not linea:
			break
		#Quitamos el uso de la cpu del script que recoge las marcas
		else:
			total = total + float(linea)


	f.close()

	res = total

#	print str(res)
	#Creamos la consulta ordenada por fecha
	con_ordenada = """select * from api_status_marcas_graficas where tipo='cpu_dia' order by fecha_hora;"""

	cursor.execute(con_ordenada)

	p = cursor.fetchall()

	
	if len(p) < num_cpu_dia:
		#insetar en al base de datos
		insert = "insert into api_status_marcas_graficas (tipo,valor) values ('cpu_dia',?);"

		cursor.execute(insert ,(res,))
		bbdd.commit()		
	else:
		#Ordenar por fecha, eliminar el ultimo e introducir nuevo
		# strftime('%d-%m-%Y  %H:%M',calldate)
		hora_actual = datetime.now()
		con_update = " update api_status_marcas_graficas set fecha_hora=datetime(?),valor=? where id=?;  "


	#	print "Antes del update, hora_actual->"+str(hora_actual)+"valor->"+str(res)+ " id->"+str(p[0][0])	
		cursor.execute(con_update ,(hora_actual,res,p[0][0]))
		bbdd.commit()
		

	##Cerramos la conexion con la BBDD
	cursor.close()
	bbdd.close()


if __name__ == "__main__":
	recoge_marcas()


