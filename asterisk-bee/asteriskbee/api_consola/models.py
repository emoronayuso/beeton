from django.db import models
from django.forms import ModelForm
# Create your models here.


class historial_comandos(models.Model):
	comando = models.CharField(max_length=500,null=True)



############Creamos el formulario a partir del modelo ##################
class historialComandosForm(ModelForm):
	class Meta:
		model = historial_comandos

