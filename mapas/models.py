from django.db import models


class Lugar(models.Model):
    nombre = models.CharField(max_length=50)
    coordenadas = models.TextField()
    centro = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Color(models.Model):
    codigo = models.CharField(max_length=20)