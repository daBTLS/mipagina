from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Pregunta, Respuesta


def index(request):
    lista_ultimas_preguntas = Pregunta.objects.order_by('-f_publicacion')[:5]
    context = {'lista_ultimas_preguntas': lista_ultimas_preguntas}
    return render(request, 'encuesta/index.html', context)


def detalle(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    return render(request, 'encuesta/detalle.html', {'pregunta': pregunta})


def resultados(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    return render(request, 'encuesta/resultados.html', {'pregunta': pregunta})


def votar(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    try:
        respuesta_seleccionada = pregunta.respuesta_set.get(pk=request.POST['respuesta'])
    except (KeyError, Respuesta.DoesNotExist):
        return render(request, 'encuesta/detalle.html', {
            'pregunta': pregunta,
            'error_message': "No seleccionaste ninguna respuesta.",
        })
    else:
        respuesta_seleccionada.votos +=1
        respuesta_seleccionada.save()
        return HttpResponseRedirect(reverse('encuesta:resultados', args=(pregunta.id)))

# Create your views here.
