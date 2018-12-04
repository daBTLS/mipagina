from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='inicio'),
    path('info', views.info, name='info'),
]
