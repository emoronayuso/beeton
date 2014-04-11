beeton
======


PASOS PARA LA INSTALACION


1) Ejecutar ./install.sh

El script de instalacion incluye: 

- La version de Asterisk 1.8.24.1, con las librerias (dependencias) libpri-1.4.14 y libss7-1.0.2 

- Django 1.5.5

- Panel de administracion Beeton


Nota importante!!
La instalacion solo se ha probado en un SO Debian 7 Wheezy (De momento).

2) Al concluir la instalación, hay que reiniciar asterisk para que se configure la nueva base de datos asocidada a los registros de llamadas "/var/log/asterisk/master.db":

   $./etc/init.d/asterisk restart

3) Para ejecutar Beeton basta con ejecutar el script ./runserver.sh de la carpeta /var/www/asterisk-bee, dandole permisos de ejecucion previamente:

   $. chmod +x runserver.sh
   
   $./runserver.sh start
   
Beeton se ejecuta en el puerto 8000 por defecto, para arrancarlo en un puerto diferente puede modificar el script de arranque runserver.sh


4) Accedemos al panel de adminsitración Beeton desde un navegador:
     
    http://<Ip_servidor>:8000
    
Nos aparecerá la ventana de login, el usuario es "admin" y la contraseña por defecto es "asteriskbee"





     
