from django.contrib import admin
from .models import Respuesta, Pregunta


class RespuestaInLine(admin.TabularInline):
    model = Respuesta
    extra = 3


class PreguntaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['texto_pregunta']}),
        ('Info. fecha', {'fields': ['f_publicacion'], 'classes': ['collapse']}),
    ]
    inlines = [RespuestaInLine]


admin.site.register(Pregunta, PreguntaAdmin)

# Register your models here.
