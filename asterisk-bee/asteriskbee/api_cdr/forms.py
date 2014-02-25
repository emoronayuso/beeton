#encoding:utf-8
from django import  forms


#Incluimos el modelo linea del contexto para crear el choice de forma dinamica

#from asteriskbee.api_dialplan.models import linea
from asteriskbee.api_dialplan.models import contextos, linea

#from datetime import date
#TIME_FORMAT = '%d/%m/%Y'


######################################
#FORMULARIO A PARTIR DE UN MODELO
#from django.forms import ModelForm
#from asteriskbee.models import <MODELOS>

#class loquesea_form(ModelForm):
#       class Meta:
#               model = MODELO
########################################

#Herramientas de DEBUG de python####
import pdb

###USO: pdb.set_trace()
###(pdb) <pulsar n para siguiente>



#Fields of forms-->https://docs.djangoproject.com/en/1.5/ref/forms/fields/

CANALES = ( ('SIP','SIP',), ('IAX','IAX',), ('DADHI','DADHI',), )

#CONTEXTOS = lista_contextos

####CREADOR DE CHOICES#####################
#creator_choices = [(c.id, c.username) for c in Group.objects.get(name__icontains='creator').user_set.all()]
#    maintainer_choices = [(m.id, m.username) for m in Group.objects.get(name__icontains='maintainer').user_set.all()]

#    creator = forms.ChoiceField(required=True, label='Project creator', choices=creator_choices)
#    maintainer = forms.MultipleChoiceField(required=True, label='Project maintainer(s)', choices=maintainer_choices)

#time_widget = forms.widgets.TimeInput(attrs={'class': 'time-pick'})

#pdb.set_trace()

#Formulario para consultas cdr
class consulta_cdr_form(forms.Form):


#	CONTEXTOS = [( c['context'], c['context'] ) for c in linea.objects.values('context').distinct() ] 

	CONTEXTOS = [( c['context'], c['context'] ) for c in linea.objects.values('context').distinct() ] 	 
	CONTEXTOS.insert(0,['*','TODOS'])

	contexto = forms.ChoiceField(choices=CONTEXTOS, required=False)

#	fecha_inicio = forms.DateField(label=u'Fecha Inicio',required=False,help_text='aaaa-mm-dd')
#	fecha_inicio = forms.DateField(label=('Fecha Inicio'), initial=lambda: datetime.now() ) 	
       
#	fecha_fin = forms.DateField(label=u'Fecha Fin',required=False,help_text='aaaa-mm-dd')
        
	duracion_mas_de = forms.IntegerField(label='La llamada dura mas de:',help_text='minutos',required=False)
	duracion_menos_de = forms.IntegerField(label='La llamada dura menos de:',help_text='minutos',required=False)
	#duracion = forms.TimeField(required=False, widget=time_widget, help_text='ex: 10:30')
        #canal = forms.ChoiceField(choices=CANALES,required=False)
	extension_de = forms.CharField(label='Extension llamante',required=False)

