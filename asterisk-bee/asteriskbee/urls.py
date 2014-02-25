from django.conf.urls import patterns, include, url
from asteriskbee.views import current_datetime,lee_y_muestra_sip
#from asteriskbee.vistas_cdr import cdr
from django.conf import settings
from api_consola.views import *
from api_status.views import *
from api_extensiones.views import *
from api_cdr.views import cdr, llamadas_pdf, generar_pdf
from api_dialplan.views import *
from api_admin_audio.views import *
from api_musica_espera.views import *
from api_admin_func.views import *


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^time/$',current_datetime),
    (r'^leesip/$',lee_y_muestra_sip),
###############PROYECTO######################
    (r'^$','asteriskbee.views.home'),
    (r'^usuario/nuevo/$','asteriskbee.views.nuevo_usuario'),
    (r'^login/$','asteriskbee.views.ingresar'),
    (r'^admin/$','asteriskbee.views.admin'),
    (r'^cerrar/$','asteriskbee.views.cerrar'),
    (r'^admin/status/$',server_status),
    (r'^admin/cdr/$',cdr),
    (r'^admin/cdr/generar_pdf/$',generar_pdf),
    (r'^admin/consola/$',consola),
    (r'^admin/consola/historial_consola/$',histo_comandos), 
    (r'^admin/status/carga_cpu/$',carga_cpu),
    (r'^admin/status/uso_ram/$',uso_ram),
    (r'^admin/status/uso_sist_raiz/$',uso_sist_fich_raiz),
    (r'^admin/status/genera_grafica_uso_cpu_dia/$',grafica_uso_cpu_dia),
    (r'^admin/status/lista_ext_reg/$',lista_extensiones_reg),
    (r'^admin/status/shutdown/$',shutdown),
    (r'^admin/sip/$',ext_sip),
    (r'^admin/sip/crear_sip/$',add_sip),
    (r'^admin/sip/mod_sip/$',mod_sip),
    (r'^admin/sip/del_sip/$',del_sip),
    (r'^admin/iax/$',ext_iax),
    (r'^admin/iax/crear_iax/$',add_iax),
    (r'^admin/iax/mod_iax/$',mod_iax),
    (r'^admin/iax/del_iax/$',del_iax),	
    (r'^admin/status/llamadas_activas/$',llamadas_activas),
    (r'^admin/dialplan/$',lista_contextos),
    (r'^admin/dialplan/crear_contexto/$',add_contexto),
    (r'^admin/dialplan/mod_contexto/$',mod_contexto),
    (r'^admin/dialplan/mod_contexto/add_linea/',carga_datos_nueva_linea),
    (r'^admin/dialplan/mod_contexto/mod_linea_comentada/',mod_linea_comentada),
    (r'^admin/dialplan/mod_contexto/borra_linea/',borra_linea),
    (r'^admin/dialplan/mod_contexto/cambia_linea/',cambia_linea),
    (r'^admin/admin_audio/$',admin_audio),
    (r'^admin/admin_audio/borra_audio/$',borra_audio),
    (r'^admin/moh/$',admin_moh),
    (r'^admin/moh/borra_moh/$',borra_moh),
    (r'^admin/admin_func/$',add_func),
    #Para los archivos de hojas de estilo
    (r'css/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.STATIC_ROOT + 'templates/css'}),
    (r'images/(?P<path>.*)$', 'django.views.static.serve', 
    {'document_root': settings.STATIC_ROOT + 'templates/images'}),
    (r'js/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.STATIC_ROOT + 'templates/js'}),
    (r'ficheros_moh/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.STATIC_ROOT + 'templates/ficheros_moh'}),

###########################################
    # Examples:
    # url(r'^$', 'asteriskbee.views.home', name='home'),
    # url(r'^asteriskbee/', include('asteriskbee.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
