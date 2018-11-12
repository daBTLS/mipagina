from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='mapa'),
    path('prueba', views.prueba, name='prueba'),
    # re_path('^(?P<pregunta_id>[0-9]+)/$', views.detalle, name='detalle'),
]
