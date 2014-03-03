#!/usr/bin/env python2.6

from pyst.agi import *
import sys

#importamos las funciones basicas de acceso a la base de datos
from funciones_basicas import *

def moh():

        miagi = AGI()

        ###Sacamos el id de la linea
        id_linea = get_id_linea(miagi.env['agi_context'],miagi.env['agi_extension'],miagi.env['agi_priority'])

        ##Comprobamos antes que la linea NO este comentada
        if get_commented_linea(id_linea) == '0':

                miagi.verbose("--------------Sistema de musica en espera--------------")
                #ext_dest = miagi.env['agi_extension']
                #tipo_ext_dest = miagi.env['agi_type']
                #callerId = miagi.env['agi_callerid']
                #cad = "---->Llamada desde--->"+callerId+" hacia--->"+ext_dest
                #miagi.verbose("Llamada desde----> %s" % callerId )
                #miagi.verbose("%s" % cad)
                #opcion_dial = tipo_ext_dest + '/' + ext_dest

                ##probamos sacar el numero de parametros
                num_para = get_num_param(id_linea)

                ####lista_de_parametros, en este caso solo uno param1 que hace 
                #### referencia al nombre de la moh
                lista = get_lista_param(id_linea)

                #######################################################################################
                ###VER VARIABLES DE ENTORNO ASTERISK INTERESANTE                                      #
                ###http://www.voip-info.org/wiki/view/Asterisk+variables                              #
                #                                                                                     #
                #estado_de_la_llamada = miagi.get_variable('DIALSTATUS')                              #
                #miagi.verbose("El estado de la llamada es:-------->> %s" % str(estado_de_la_llamada))#
                #                                                                                     #
                #Si el estado de la llamada es ocupado ejecutamos la musica en espera                 #
                #if estado_de_la_llamada == 'BUSY':                                                   #
                ####################################################################################### 

                #miagi.verbose("---------musica en espera------")
                if str(lista[0]) != "":
                        miagi.appexec('setMusicOnHold',str(lista[0]))

                miagi.verbose("-----------------------------------------------------------")

        else:
                cad = "ESTA COMENTADA! - La linea de musica en espera del contexto->"+miagi.env['agi_context']+ " de la extencion->"+miagi.env['agi_extension']+" y prioridad->"+miagi.env['agi_priority']

                miagi.verbose("%s" % cad)


if __name__ == "__main__":
        moh()