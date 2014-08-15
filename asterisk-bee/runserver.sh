#!/bin/bash

if [ $# -eq 0 ] || [ $# -gt 1 ]; then
   echo "USO:"
   echo "Arrancar Beeton: ./runserver.sh start" 
   echo "Detener Beeton: ./runserver.sh stop"
else
   if [ $1 == "start" ]; then
     #python manage.py runserver 0.0.0.0:8000
     screen -S runserver_beeton -d -m python manage.py runserver 0.0.0.0:8000 
     sleep 2
     HTTPS=1 screen -S runserver_beeton_ssl -d -m python manage.py runsslserver 0.0.0.0:8001
     sleep 3
     echo "Beeton se ha iniciado" 
   elif [ $1 == "stop" ]; then
     pid=`netstat -lpn | grep 8000 | tr -s ' ' '-' | cut -d '-' -f7 | cut -d '/' -f1` 
     kill -9 $pid
     pid=`netstat -lpn | grep 8001 | tr -s ' ' '-' | cut -d '-' -f7 | cut -d '/' -f1` 
     kill -9 $pid
     echo "Beeton se ha parado"
   else
     echo "Opcion incorrecta"
   fi
fi
