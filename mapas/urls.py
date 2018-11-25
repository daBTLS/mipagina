from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='mapa'),
    path('prueba', views.prueba, name='pruebaM'),
    path('detalle/<str:sec>', views.detalle, name='detalle'),
]
