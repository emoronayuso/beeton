#!/bin/bash
# -*- ENCODING: UTF-8 -*-

cd /home/asterisk-bee/asteriskbee/api_status/scripts_graficas/temp/

top -n 1 > temp_cpu_dia
sed -i '1,7d' temp_cpu_dia
cat temp_cpu_dia | tr ' ' '-' | tr -s '-' | cut -d '-' -f 10 > temp_cpu_dia2
 
