#!/bin/bash

#echo -e "En que directorio dese hacer la instalación (Indice la ruta absoluta):"
#read directory

dir_actual=$(pwd)

##
dir_insta='/var/www'
#cd $dir_insta'/asterisk-bee'


apt-get update

apt-get install --assume-yes screen

echo -e "-> Instalacion de Asterisk <- "
apt-get install --assume-yes build-essential


cd /usr/src
wget http://downloads.asterisk.org/pub/telephony/libpri/releases/libpri-1.4.14.tar.gz
wget http://downloads.asterisk.org/pub/telephony/libss7/releases/libss7-1.0.2.tar.gz

wget http://downloads.asterisk.org/pub/telephony/asterisk/releases/asterisk-1.8.24.1.tar.gz

tar -xzvf /usr/src/libpri-1.4.14.tar.gz
tar -xzvf /usr/src/libss7-1.0.2.tar.gz
tar -xzvf /usr/src/asterisk-1.8.24.1.tar.gz

rm -r *.tar.gz

/usr/src/asterisk-1.8.24.1/contrib/scripts/install_prereq install

/usr/src/asterisk-1.8.24.1/contrib/scripts/install_prereq install-unpackaged

cd /usr/src/libpri-1.4.14
make
make install

cd /usr/src/libss7-1.0.2
make
make install

cd /usr/src/asterisk-1.8.24.1
./configure
make menuselect
make
make install

make config

make samples

########Iniciando asterisk#########################
echo "---------Iniciando Asterisk por primera vez -----------"
cd /etc/init.d/
asterisk restart
echo "-----------------------------------------------------"
####################################################

##paquetes necesarios para Asterisk Realtime#########
apt-get install --assume-yes libsqliteodbc unixodbc
#####################################################






##############################################INSTALACION DE DJANGO 1.5.5#############################
echo -e "-> Instalando Django 1.5.5 <-"

apt-get install --assume-yes python-setuptools

cd $dir_actual/files

tar -zxvf Django-1.5.5.tar.gz

cd Django-1.5.5

python setup.py install
####################################################################################################


##########################################################INSTALACION DE BEETON#############################
echo -e "-> Instalando Asterisk BEETON <-"

apt-get install --assume-yes python-setuptools

apt-get install --assume-yes python-pip

pip install flup



####Instalacion de modulos necesarios para generar graficas##
easy_install -U distribute

apt-get install --assume-yes python-dev

pip install matplotlib

#pip install python-crontab
#############################################################

#pip install pisa

pip install django-sslserver

pip install html5lib

cd $dir_actual

python setup.py install

cd /usr/local/lib/python2.7/dist-packages/django_beeton-0.1-py2.7.egg

cp -Rp asterisk-bee $dir_insta

cd $dir_insta/asterisk-bee

ln -s  /var/lib/asterisk/sqlite.db db_asteriskbee_sqlite.db

cd asteriskbee

#ln -s /var/lib/asterisk/agi-bin agi_bin

cd $dir_actual/files/

#cp -Rp agi-bin/* $dir_insta/asterisk-bee/asteriskbee/agi_bin

cp db/sqlite.db /var/lib/asterisk/

cp -Rp etc/odbc.ini /etc/
cp -Rp etc/odbcinst.ini /etc/

###Ficheros de config de Asterisk#####
cp  etc/asterisk/extconfig.conf /etc/asterisk/
cp  etc/asterisk/res_odbc.conf /etc/asterisk/
cp  etc/asterisk/res_config_sqlite.conf /etc/asterisk/
cp  etc/asterisk/modules.conf /etc/asterisk/
cp  etc/asterisk/cdr_sqlite3_custom.conf /etc/asterisk/
cp  etc/asterisk/extensions.conf /etc/asterisk/
touch /etc/asterisk/beeton_extensions.conf
######################################

cd $dir_insta/asterisk-bee/asteriskbee/api_cdr
mkdir bbdd
cd bbdd
ln -s /var/log/asterisk/master.db cdr.db

cd $dir_insta/asterisk-bee/asteriskbee/api_admin_audio
ln -s /var/lib/asterisk/sounds/en sonidos

cd $dir_insta/asterisk-bee/asteriskbee/templates
ln -s $dir_insta/asterisk-bee/asteriskbee/api_musica_espera/ficheros_audio/ ficheros_moh

cd $dir_actual/files/
cp audios_de_muestra/* /var/lib/asterisk/sounds/en/

cd $dir_insta/asterisk-bee/asteriskbee/api_musica_espera/
mkdir ficheros_audio
####################################################################################



#####Se vuelve a reiniciar para que Asterisk genere la base de datos del cdr (master.db)###
cd /etc/init.d/
asterisk restart
######################################################################

#######Se genera el enclace simbolico a los sripts AGI########
cd $dir_insta/asterisk-bee/asteriskbee/
ln -s /var/lib/asterisk/agi-bin agi_bin

cd $dir_actual/files/
cp -Rp agi-bin/* $dir_insta/asterisk-bee/asteriskbee/agi_bin


#########se instala python-crontab######
##Necesario para script crontab de graficas#########
cd $dir_actual
wget https://pypi.python.org/packages/source/p/python-crontab/python-crontab-1.7.2.tar.gz
tar -zxvf python-crontab-1.7.2.tar.gz
cd python-crontab-1.7.2
python setup.py install

cd $dir_insta/asterisk-bee/asteriskbee/api_status/scripts_graficas/
python script_crontab.py
#####################################################

pip install pisa
