#encoding:utf-8
from django import  forms
from django.forms import widgets


######################################
#FORMULARIO A PARTIR DE UN MODELO
#from django.forms import ModelForm
#from asteriskbee.models import <MODELOS>

#class loquesea_form(ModelForm):
#       class Meta:
#               model = MODELO
########################################

#Fields of forms-->https://docs.djangoproject.com/en/1.5/ref/forms/fields/

#CANALES = ( ('SIP','SIP',), ('IAX','IAX',), ('DADHI','DADHI',), )

#Formulario para envio del comando a la consola
class consola_form(forms.Form):
	comando = forms.CharField(label='Comando',required=False)
#	comando =forms.TextInput(attrs={'size': 10,'label':'Comando', }) #input tipo text
#        fecha_inicio = forms.DateField(label='Fecha Inicio',required=False)
#        fecha_fin = forms.DateField(label='Fecha Fin',required=False)
#        duracion = forms.IntegerField(label='La llamada dura mas de:',help_text='minutos',required=False)
#        canal = forms.ChoiceField(choices=CANALES,required=False)

#class consola_form(forms.Form):
#		comando = forms.CharField(label='Comando')
#		comando.TextInput(attrs={'size': 10, }) 


