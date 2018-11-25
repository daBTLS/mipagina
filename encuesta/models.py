from django.db import models

# the following lines added:
import datetime
from django.utils import timezone


class Pregunta(models.Model):
    texto_pregunta = models.CharField(max_length=200)
    f_publicacion = models.DateTimeField('date published')

    def __str__(self):
        return self.texto_pregunta

    def publicado_reciente(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.f_publicacion <= now

    publicado_reciente.admin_order_field = 'pub_date'
    publicado_reciente.boolean = True
    publicado_reciente.short_description = 'Published recently?'


class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.DO_NOTHING, )
    texto_respuesta = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.texto_respuesta
