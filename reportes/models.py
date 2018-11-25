from django.db import models


class Color(models.Model):
    c1 = models.CharField(max_length=20)
    c2 = models.CharField(max_length=20)
