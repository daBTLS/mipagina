from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse


# from .models import Pregunta, Respuesta

def index(request):
    maps_key = 'AIzaSyDOasrsHgzaVmIbGhWyPherFl7DNgOcSHM'
    context = {'maps_key': maps_key}
    return render(request, 'mapas/mapa.html', context)


def prueba(request):
    context = {'dias': [1, 2, 3], }
    return render(request, 'mapas/prueba.html', context)
