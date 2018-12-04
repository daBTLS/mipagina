from django.http import HttpResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.db import connection
from .models import Color

import random
import datetime


def index(request):
    maps_key = 'AIzaSyDOasrsHgzaVmIbGhWyPherFl7DNgOcSHM'
    context = {'maps_key': maps_key}
    return render(request, 'reportes/reporte.html', context)


def prueba(request):
    labels = []
    fecha = ''
    data = ''
    bColor = []
    hColor = []
    lista = []
    meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE",
             "NOVIEMBRE", "DICIEMBRE"]
    sc = "select dl.id_grupo, dl.delito, coalesce(count(*), 0) from mensajes, ctlgo_delito dl cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where d.delito = dl.id_grupo group by dl.delito, dl.id_grupo order by dl.id_grupo"
    with connection.cursor() as cursor:
        cursor.execute(sc)
        rows = cursor.fetchall()
        max = len(rows)
        listaColores = getRandomColors(max)
        i = 0
        for row in rows:
            labels.append(row[1])
            data = data + str(row[2]) + ', '
            bColor.append(listaColores[i].c1)
            hColor.append(listaColores[i].c2)
            i = i + 1
    script = "select dl.delito, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '01' and d.delito = dl.id_grupo) as enero, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '02' and d.delito = dl.id_grupo) as febrero, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '03' and d.delito = dl.id_grupo) as marzo, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '04' and d.delito = dl.id_grupo) as abril, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '05' and d.delito = dl.id_grupo) as mayo, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '06' and d.delito = dl.id_grupo) as junio, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '07' and d.delito = dl.id_grupo) as julio, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '08' and d.delito = dl.id_grupo) as agosto, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '09' and d.delito = dl.id_grupo) as septiembre, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '10' and d.delito = dl.id_grupo) as octubre, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '11' and d.delito = dl.id_grupo) as noviembre, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '12' and d.delito = dl.id_grupo) as diciembre from ctlgo_delito dl"
    with connection.cursor() as cursor:
        cursor.execute(script)
        rows = cursor.fetchall()
        max = len(rows)
        listaColores = getRandomColors(max)
        i = 0
        for row in rows:
            lista.append({'delito': row[0],
                          'data': str(row[1]) + ', ' + str(row[2]) + ', ' + str(row[3]) + ', ' + str(
                              row[4]) + ', ' + str(row[5]) + ', ' + str(row[6]) + ', ' + str(row[7]) + ', ' + str(
                              row[8]) + ', ' + str(row[9]) + ', ' + str(row[10]) + ', ' + str(row[11]) + ', ' + str(
                              row[12]),
                          'bColor': listaColores[i].c1,
                          'hColor': listaColores[i].c2})
            i = i + 1
    with connection.cursor() as cursor:
        cursor.execute("select max(fecha) from mensajes")
        row = cursor.fetchone()
        fecha = ''.join(row[0].strftime('%d / %m / %Y'))
    context = {'labels': labels, 'data': data, 'bColor': bColor, 'hColor': hColor, 'lista': lista, 'meses': meses,
               'fecha': fecha}
    return render(request, 'reportes/prueba.html', context)


def pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename = "hola.pdf"'

    p = canvas.Canvas(response)

    # DIBUJAR CONTENIDOS DEL PDF
    p.drawString(100, 100, "Hello world.")

    p.showPage()
    p.save()
    return response


def getRandomColors(num):
    l = []
    colores = Color.objects.order_by('id')
    ns = random.sample(range(len(colores)), num)
    for n in ns:
        l.append(colores[n])
    return l
