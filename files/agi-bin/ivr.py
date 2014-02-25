#!/usr/bin/env python2.6

from datetime import datetime

####Descripcion de la funcion IVR########################################################
# Se trata de un sistema de respuesta de voz interactiva, o tambien llamado operadora automatica ###
##########################################################################################
####NUMERO DE PARAMETROS : 9
####1-> Itervalo horario de manana (abierto). FORMATO: "8:00-14:00"
####2-> Intervalo horario de tarde (abierto).
####3-> Intervalo dias de la semana manana (abierto). FORMATO: "mon-fri"
####4-> Intervalo dias de la semana tarde (abierto)
####5-> Audio fuera de horario
####6-> Audio dia festivo
####7-> Audio de bienvenida con menu de opciones
####8-> Lista de opciones. FORMATO: "1-nombre_contexto1, 2-nombre_contexto2,..."
####9-> Buzon de voz en caso de lineas ocupadas. FORMATO "extension@contexto"
##########################################################################################



##Ejemplo de operadora en Dialplan: (/etc/asterisk/extensions.conf) ########

# [operadora]
# exten => s,1,NoOp
# exten => s,n,Answer()
# exten => s,n,GotoifTime(8:00-14:00,mon-fri,*,*?abierto,s,1)
# exten => s,n,GotoifTime(16:00-18:00,mon-fri,*,*?abierto,s,1)
# exten => s,n,GotoifTime(*,mon-fri,jan?festivo)
# exten => s,n,Playback(fueradehorario)
# exten => s,n,Voicemail(100@default)
# exten => s,n,Hangup()
# exten => s,n(festivo),Playback(festivo)
# exten => s,n,Voicemail(100@fedault)
# exten => s,n,Hangup()

#EXPLICACION: Esto podria ser la estructura de una eficaz 'introduccion' a nuestra operadora automatica. Leyendolo rapidamente, lo que tratamos de hacer es que salte al contexto 'abierto' en caso que la llamada se encuentre en horario lectivo de la empresa, o que salte a la etiqueta 'festivo' en caso que coincida que es dia de fiesta. En otro caso, lanzara un mensaje de 'estamos cerrados', saltara un buzon de voz para dejar mensajes y colgara, en caso que salte a la etiqueta 'festivo', algo parecido, un mensaje diciendo que es dia festivo en la empresa, buzon de voz y cuelgue.

#La funcion Goto, es equivalente, pero introduciendo una condicion temporal. Para los conocedores de Cron, esto es equivalente.

#En primera posicion, especificamos hora o rango horario, incluso varios rangos horarios. Por nuestro ejemplo podriamos haberlo resumido con:

#      exten => s,n, GotoifTime(8:00-14:00,mon-fri,*,*?abierto,s,1)
#      exten => s,n,GotoifTime(16:00-18:00,mon-fri,*,*?abierto,s,1)

#  por

#      exten => s,n,GotoifTime(8:00-14:00|16:00-18:00,mon-fri,*,*?abierto,s,1). 
#
#   Dos pajaros de un tiro como quien dice.

#El segundo parametro, es el dia de la semana, en ingles, los tres primeros caracteres, y ocurre lo mismo que con las horas, rangos, multiples rangos, etc.

#El tercer parametro, es el dia del mes y el cuarto, el mes en ingles y los tres primeros caracteres igual. El resto es equivalente a a la aplicacion Goto.

#Ademas aqui hemos introducido las etiquetas aparte de los contextos. Una etiqueta se ubica en una parte de la prioridad, esto es util cuando como ocurre en mis ejemplos en vez de poner prioridades del tipo, 1 2 3, etc pongo siempre n considerando lo de n+1 y queremos saltar a otra prioridad sin tener que saber la posicion relativa (esto nos permite la maxima genericidad en nuestros planes de marcacion y la capacidad de insercion futura en casos complejos).

#Sobre los ultimos dos parametros, dia del mes y mes, hay que considerar que esto permite mucho 'poder' para crear genericidad a lo largo de los anos, como son el caso de los dias festivos. En nuestro ejemplo decimos: Si es lunes a viernes y ademas cae el 1 de Enero entonces es festivo. Aunque sea lo que sea realmente es festivo este seria un ejemplo especifico de la posibilidad saltar al contexto dia festivo realmente en estos dias, y si fuera un sabado o un domingo, como ya es festivo de por si, que de el otro mensaje (El de cerrado simplemente) . Opciones hay muchas y esto quedaria a nuestra libertad.

#Mas alla aun, asterisk 1.8 tengo entendido que incluso existe la posibilidad de crear calendarios con Google Calendar y desde ahi especificar los dias festivos y toda la informacion relativa a tiempos. Hay mas informacion aqui, y esto nos ofreceria un nivel de potencia a bajo coste de complejidad para nuestro IVR que ninguna otra central se acercaria lo mas minimo. Ahora ya podemos decir que estamos sobre el nivel del mar, y eso que no hemos empezado siquiera en este mundillo.

#Por otro lado, tenemos la aplicacion Playback. Simplemente reproduce un archivo de musica que tengamos en la carpeta correspondiente en funcion de nuestro lenguaje definido. Los sonidos se encuentran en /var/lib/asterisk/sounds/

#Finalmente esta la aplicacion Voicemail, que basicamente llama a otro archivo de musica ('deje su mensaje despues de oir la senal') y guarda el mensaje de voz en el buzon especificado (100) del contexto por defecto (@default). Todo esto podemos verlo y configurarlo en el archivo de configuracion voicemail.conf que seguramente veremos en otro momento.

#Y ahora que ocurre con las llamadas que van al contexto 'abierto'  

#Vamos a hacer algo sencillito en abierto para terminar por hoy, y mas adelante intentaremos profundizar aun mas en todo esto.

# [abierto]
# exten => s,1,NoOp
# exten => s,n,Background(listadistribucion)
# exten => s,n,WaitExten(20)

# exten => 1,1,NoOp
# exten => 1,n,Goto(comercial,s,1)

# exten => 2,1,NoOp
# exten => 2,n,Goto(postventa,s,1)

# exten => t,1,NoOp
# exten => t,n,Goto(telefonista,s,1)
# exten => t, n,Goto(s,1)

#Voy a leerlo: primero, saltaria un mensaje, que diria 'Bienvenido a nuestra empresa, Marque el 1 para hablar con Comercial o Marque el 2 para hablar con Posventa, en otro caso espere y le pondremos con un Agente'. En caso de marcar el 1, le mandaria al contexto comercial, y en caso de marcar el 2, a postventa. En caso de 'Timeout simple' le mandaria al telefonista.

#Aqui solo tenemos dos aplicaciones que no vimos hasta el momento:

#Background es equivalente a Playback pero deja a la espera de marcacion de una extension. Podemos interrumpir el background si marcamos teclas en el telefono y saltaria a la extension del contexto marcada (hay mas opciones complejas, como saltar a extensiones de otros contextos pero no voy a entrar en detalles)

#Por otro lado Waitexten, basicamente establece el tiempo que tenemos para marcar una extension antes de ir a la extension especial 't'.

#Parece sencillo, y lo es. Asi que invito a hacer mil combinaciones con toda esta informacion para crear posibles IVR sencillitos que cumplan una funcion que para la mayoria de las PBX del mercado suele ser bastante compleja y obliga a pasar por miles de secciones de la interfaz grafica. Por esto, es suficiente por hoy. Seguiremos informando como suele decirse



##############################################################################################

from pyst.agi import *

#importamos las funciones basicas de accesos a la base de datos
from funciones_basicas import *


##Lista de aplicaciones de asterisk http://www.voip-info.org/wiki/view/Asterisk+-+documentation+of+application+commands

def ivr():

	##Lo primero sera sacar el contexto, la extension del receptor de la llamada y
	## la prioridad para sacar la id de la linea del dialplan
	## para ello accedemos a las variables de entorno: agi_context, agi_extension, agi_priority 

	
	miagi = AGI()
	miagi.verbose("--------------SISTEMA DE IVR--------------")
	ext_dest = miagi.env['agi_extension']
        tipo_ext_dest = miagi.env['agi_type']
	callerId = miagi.env['agi_callerid']

	###Sacamos el id de la linea
	id_linea = get_id_linea(miagi.env['agi_context'],miagi.env['agi_extension'],miagi.env['agi_priority'])

	##Comprobamos antes que la linea NO este comentada
	if get_commented_linea(id_linea) == '0':

		##sacamos el numero de parametros
		num_para = get_num_param(id_linea)

		####lista_de_parametros########## 
		####1-> Itervalo horario de manana (abierto). FORMATO: "8:00-14:00"
		####2-> Intervalo horario de tarde (abierto).
		####3-> Intervalo dias de la semana manana (abierto). FORMATO: "mon-fri"
		####4-> Intervalo dias de la semana tarde (abierto)
		####5-> Audio fuera de horario
		####6-> Audio dia festivo
		####7-> Audio de bienvenida con menu de opciones
		####8-> Lista de opciones. FORMATO: 1-[contexto_opcion_1]/[extension_opcion_1]/[prioridad_opcion_1],2-.....,
		####9-> Buzon de voz en caso de lineas ocupadas. FORMATO "extension@contexto"
		lista = get_lista_param(id_linea)

		##################################
		##String con formato: 08:00-15:00
		int_hora_manana = str(lista[0])
		int_hora_tarde  = str(lista[1])
		###################################

		##String con formato: Lunes-Viernes
		int_dias_manana = str(lista[2])
		int_dias_tarde  = str(lista[3])
		##################################
		
		##String del nombre del audio (sin extension)
		audio_fuera_hora = str(lista[4])
		audio_dia_festivo = str(lista[5])
		audio_menu_opciones = str(lista[6])	


		##########################################################################################
		##String con formato: 1-[contexto_opcion_1]/[extension_opcion_1]/[prioridad_opcion_1],2-.....,
		string_lista_opciones = str(lista[7])
		#########################################################################################



		dic = {}

		li = string_lista_opciones.split(',')
		
		#miagi.verbose("---el tamano de la lista es %d ----" % len(li) )

		##Recogemos la informacion en un diccionario para facilitar el manejo. 
		## FORMATO: dic{ [1] : ['usuarios','123','1'], [2]:['operadora','125','1'], ... }
		for i in range(len(li)-1):
			dic[int(li[i].split('-')[0])] = li[i].split('-')[1].split('/')

		######Acceso a los datos ##################
		## El contexto de la opcion 2 ->  dic[2][0]
		## La extension de le opcion 3 ->  dic[3][1]
		## La prioridad de la opcion 1  -> dic[1][2]	
		#######################################################################################
		buzon_de_voz = str(lista[8])

		#miagi.verbose("---Se ejecuta esta linea----")
		

		# [operadora]
		# exten => s,1,NoOp
		# exten => s,n,Answer()
		miagi.appexec('Answer')
		# exten => s,n,GotoifTime(8:00-14:00,mon-fri,*,*?abierto,s,1)
	#	miagi.appexec('GotoifTime','8:00-14:00,mon-fri,*,*?abierto,s,1')
		# exten => s,n,GotoifTime(16:00-18:00,mon-fri,*,*?abierto,s,1)
	#	miagi.appexec('GotoifTime','16:00-18:00,mon-fri,*,*?abierto,s,1')
		# exten => s,n,GotoifTime(*,mon-fri,jan?festivo)
	#	miagi.appexec('GotoifTime','*,mon-fri,jan?festivo')
		# exten => s,n,Playback(fueradehorario)
		#miagi.appexec('Playback','prueba_ee_8')


#		string_fecha = '2008-11-10 17:53'
#		datetime.datetime.strptime('2008-11-10 17:53', '%Y-%m-%d %H:%M')

		#fecha = datetime.strptime('2013-12-29 17:53', '%Y-%m-%d %H:%M')
		#miagi.verbose("La fecha hecha es ----> %s" % str(fecha) )
		#datetime.now()   -> Fechahora actual


#######################################DIA DE LA SEMANA #######################################################
		dicDays = {'MONDAY':'Lunes','TUESDAY':'Martes','WEDNESDAY':'Miercoles','THURSDAY':'Jueves', \
                           'FRIDAY':'Viernes','SATURDAY':'Sabado','SUNDAY':'Domingo'}

		dicDiasnum = {'Lunes' : 1, 'Martes' : 2, 'Miercoles' : 3, 'Jueves' : 4, 'Viernes': 5, 'Sabado' : 6, 'Domingo' : 7 }

	
	#	int_dias = "Lunes-Viernes"
		## Inicilizamos a 0 el numero de la semana si no hay ningun intervalo, tanto de tarde como de manana
		num_dia_de_manana = 0
		num_dia_a_manana  = 0 
		num_dia_de_tarde  = 0
		num_dia_a_tarde   = 0
	

		#miagi.verbose("el intervalo de dias de manana es ----> %s" % str(int_dias_manana) )
		#miagi.verbose("el intervalo de dias de tarde es ----> %s" % str(int_dias_tarde) )

		##Si hay algun intervalo definido, suponemos que tiene el formato adecuado
		if int_dias_manana != "":	
			dias_manana = int_dias_manana.split('-')
			#Sacamos el numero del dia de los intervalosde manana y tarde
			num_dia_de_manana = dicDiasnum[dias_manana[0]] 
			num_dia_a_manana  = dicDiasnum[dias_manana[1]]


		if int_dias_tarde != "":
			dias_tarde = int_dias_tarde.split('-')		
			num_dia_de_tarde =  dicDiasnum[dias_tarde[0]]
			num_dia_a_tarde =  dicDiasnum[dias_tarde[1]]

	

		#miagi.verbose("El numero del dia de - es-----> %s " % dicDiasnum[dias[0]] )
		#miagi.verbose("El numero del dia a - es-----> %s " %  dicDiasnum[dias[1]] )
	 
		#miagi.verbose("wewewewewewewe  --->>> %s " %  dicDiasnum[dicDays[fecha.strftime('%A').upper()]] )


		#miagi.verbose("El  dia de la semana y su nuemro es-----> %s " % dicDays[fecha.strftime('%A').upper()])

		##Sacamos el dia de la semana del dia actual
		fecha_actual = datetime.now()

		#miagi.verbose("la fecha actual es----> %s" % str(fecha_actual.strftime('%Y-%m-%d %H:%M')) )


		##############Aqui esta el error#############
		#miagi.verbose("----------------------->>>>>>> %s " % str( dicDays[fecha_actual.strftime('%A').upper()] ) )

		dia_semana_fecha_actual = dicDays[fecha_actual.strftime('%A').upper()]

	#	miagi.verbose("el dia de la semana de hoy es ----> %s" % str(dia_semana_fecha_actual) )

		#Sacamos el numero del dia de la semana de la fecha actual
		num_dia_actual = dicDiasnum[dia_semana_fecha_actual]

	#	miagi.verbose("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW ---->" )

###############################################################################################################

################################### Intervalos horarios ###################################################
		##Construir rango FORMATO 8:00-14:00, mon-fri, 

		if int_hora_manana != "":


			hora_manana = {}
			hora_manana = int_hora_manana.split('-')


			hora_manana_ini = datetime.strptime(hora_manana[0], '%H:%M')
			hora_manana_fin = datetime.strptime(hora_manana[1], '%H:%M')



	
			hora_actual = datetime.now()
			miagi.verbose("--->La hora actual es: %s" % str(hora_actual.strftime('%H:%M')))
	#               int_hora_tarde  = str(lista[1])
		
		if int_hora_tarde != "":
			hora_tarde = {}
			hora_tarde = int_hora_tarde.split('-')

			hora_tarde_ini = datetime.strptime(hora_tarde[0], '%H:%M')
			hora_tarde_fin = datetime.strptime(hora_tarde[1], '%H:%M')
	#               int_dias_manana = str(lista[2])  FORMATO: "Lunes-Viernes"
	#               int_dias_tarde .....



###############################################################################################################


################################LOGICA DEL IVR ###########################################################

		miagi.verbose("HORARIO MAnANA de:  %s " % str(hora_manana_ini.strftime('%H:%M')) )
		miagi.verbose("               a :  %s " % str(hora_manana_fin.strftime('%H:%M')) )

		miagi.verbose("HORARIO TARDE de:  %s " % str(hora_tarde_ini.strftime('%H:%M')) )
		miagi.verbose("               a:  %s " % str(hora_tarde_fin.strftime('%H:%M')) )

		miagi.verbose("HORA ACTUAL:  %s " % str(datetime.now().strftime('%H:%M')) )


		hora_actual = datetime.now().strftime('%H:%M')

         ##Si esta dentro del intervalo de manana, solo comparamos la hora, usando el strftime
         ## ya que la fecha por defecto es: 1900-01-01 
		if hora_manana_ini.strftime('%H:%M') < hora_actual and hora_actual < hora_manana_fin.strftime('%H:%M'):
		#	miagi.appexec('Playback','prueba_ee_8')	
			miagi.verbose("ES POR LA MANANA")

			#Si es horario de manana comprabamos el dia de la semana
			# num_dia_actual tiene que estar en el rango
			if num_dia_actual in range(num_dia_de_manana,num_dia_a_manana+1):
				miagi.verbose("ES DIA DE LA SEMANA DE MANANA")

		## Si no si esta dentro del intervalo de tarde
		elif hora_tarde_ini.strftime('%H:%M') < hora_actual and hora_actual < hora_tarde_fin.strftime('%H:%M'):
	#		miagi.appexec('Playback','prueba_ee_8')
			miagi.verbose("ES POR LA TARDE")
	
			if num_dia_actual in range(num_dia_de_tarde,num_dia_a_tarde+1):
				miagi.verbose("ES DIA DE LA SEMANA DE TARDE")

			

		##Si no esta fuera de horario
		else:
			miagi.verbose("ESTA FUERA DE HORARIO - %s " % str(datetime.now().strftime('%H:%M')) )


		# exten => s,n,Voicemail(100@default)
		# exten => s,n,Hangup()
		# exten => s,n(festivo),Playback(festivo)
		# exten => s,n,Voicemail(100@fedault)
		# exten => s,n,Hangup()
		
		# [abierto]
		# exten => s,1,NoOp
		# exten => s,n,Background(listadistribucion)
		
		#miagi.stream_file('menu_opciones', [1,2,3,4,5,6,7,8,9,0,'#','*'])

###############################################################################
		while True:		
			##Funcion que reproduce el audio a la espera de la pulsacion de alguno de los diginos pasados como parametros o hasta un timeout em ms (por defecto 5000 ms), y devuelve la opcion elegida
			opcion_elegida = miagi.get_option(audio_menu_opciones,[1,2,3,4,5,6,7,8,9,0,'#','*'],10000)
			##Repetimos el mensaje si el usuario pulsa la tecla '*'
			if opcion_elegida != '*':
				break
##############################################################################
		#miagi.verbose("---LA OPCION ELEGIDA ES --->> %s <<<----" % opcion_elegida)

		##Si el usuario pulsa '0' pedimos al usuario que marque la extension 
		if opcion_elegida == '0':
			extension_marcada = miagi.get_data('introduce_exten')
			##Si la extension no existe reproducir 'exten_correcta.gsm'
		
			miagi.goto_on_exit('usuarios',extension_marcada,1)
		else:
			##Funcion que salta al contexto/exten/prioridad determinada al salir#####
			##El contexto de la opcion 2 ->  dic[2][0]
                	##La extension de le opcion 3 ->  dic[3][1]
                	##La prioridad de la opcion 1  -> dic[1][2]
			miagi.goto_on_exit(dic[int(opcion_elegida)][0],dic[int(opcion_elegida)][1],dic[int(opcion_elegida)][2])
			#######################################################################
	

		#miagi.appexec('Background','menu_opciones')
		# exten => s,n,WaitExten(20)

		# exten => 1,1,NoOp
		# exten => 1,n,Goto(comercial,s,1)

		# exten => 2,1,NoOp
		# exten => 2,n,Goto(postventa,s,1)

		# exten => t,1,NoOp
		# exten => t,n,Goto(telefonista,s,1)
		# exten => t, n,Goto(s,1)

	#	miagi.appexec('Playback','conf-usermenu')		


	#	miagi.appexec('GotoifTime', '8:00-14:00,mon-fri,*,*?abierto,101,1')
	#	miagi.appexec('GotoifTime','16:00-18:00,mon-fri,*,*?operadora,101,1')

#		cad = "La extension llamante "+tipo_ext_dest+"/"+callerId+" tiene que esperar X segundos al llamar a la extension destino "+ext_dest + "WEEEEEE---->>>>>"+ miagi.env['agi_context']+"--"+miagi.env['agi_extension']+"--"+miagi.env['agi_priority']+"--IDLINEA--->"+id_linea+"-----NUM PARAMETROS-----"+num_para+"--pepeeeL-->"+lista[0]

		#miagi.verbose("Llamada desde----> %s" % callerId )
#		miagi.verbose("%s" % cad)
		#### El parametro de segundo de la espera
#		opcion_wait = str(lista[0])
		#miagi.verbose("-------->  %s " % opcion_dial)
		#miagi.answer()
		#miagi.stream_file('demo-congrats')
		#miagi.appexec('noop',"Llamada desde %s opciones -> %s" % callerId,opcion_dial)
		#miagi.noop()
		#miagi.appexec('Wait', opcion_wait)
		miagi.verbose("-----------------------------------------------------------")
		#miagi.hangup()
	
	else:

		cad = "ESTA COMENTADA! - La linea de ivr del contexto->"+miagi.env['agi_context']+ " de la extencion->"+ext_dest+" y prioridad->"+miagi.env['agi_priority']

		miagi.verbose("%s" % cad)


if __name__ == "__main__":
	ivr()
