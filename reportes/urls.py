from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='reporte'),
    path('pdf', views.pdf, name='pdf'),
    path('<str:sec>', views.index, name='reporte'),
    path('prueba', views.prueba, name='pruebaR'),
]
