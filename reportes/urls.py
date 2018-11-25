from django.urls import path
from . import views

urlpatterns = [
    path('', views.prueba, name='reporte'),
    path('prueba', views.prueba, name='pruebaR'),
    path('pdf', views.pdf, name='pdf'),
]
