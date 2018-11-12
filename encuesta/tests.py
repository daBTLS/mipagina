import datetime
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from .models import Pregunta


def crear_pregunta(texto_pregunta, dias):
    t = timezone.now() + datetime.timedelta(days=dias)
    return Pregunta.objects.create(texto_pregunta=texto_pregunta, f_publicacion=t)


class VerPreguntaTests(TestCase):
    def test_index_view_sin_preguntas(self):
        """
            If no questions exist, an appropriate message should be displayed.
        """
        r = self.client.get(reverse('index'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "No hay encuestas disponibles.")
        self.assertQuerysetEqual(r.context['lista_ultimas_preguntas'], [])
