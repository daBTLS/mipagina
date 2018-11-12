from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path('^(?P<pregunta_id>[0-9]+)/$', views.detalle, name='detalle'),
    re_path('^(?P<pregunta_id>[0-9]+)/results/$', views.resultados, name='resultados'),
    re_path('^(?P<pregunta_id>[0-9]+)/vote/$', views.votar, name='votar'),
]
