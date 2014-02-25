from crontab import CronTab
from django.conf import settings

#####################################################
###Para mas info sobre el uso de python-crontab######
### https://pypi.python.org/pypi/python-crontab ######
#####################################################

##Directorio de la aplicaion
### STATIC_ROOT = '/var/www/asterisk-bee/asteriskbee/'
directorio = settings.STATIC_ROOT+"api_status/scripts_graficas/"

tab = CronTab(user='root')
#cmd = 'python '+directorio+'recoge_marcas_graficas.py > /root/peeeeeee'

#cmd = '/bin/bash top.sh'

#cmd = '/bin/bash /home/asterisk-bee/asteriskbee/api_status/scripts_graficas/top.sh'


cmd = 'python '+directorio+'recoge_marcas_graficas.py >/dev/null 2>&1'
#############INCLUIR UNA TAREA AL CRON ##################
#cron_job = tab.new(cmd)

##Una tarea se lanzara cada vez que se inice la centralita
#cron_job.every_reboot()

#### Otra tarea cada 5 minutos #
#cron_job.minute.every(2)


#Escribe el contenido al archivo de cron
#tab.write()

##Mostramos la nueva linea que se incluira en el archivo de cron
print tab.render()
##############################################


##PARA BORRAR UNA TAREA#############
#cron_job = tab.find_command(cmd)

#tab.remove_all(cmd) 
#Escribe el contenido al archivo de cron
#tab.write()

#print tab.render()
####################################

