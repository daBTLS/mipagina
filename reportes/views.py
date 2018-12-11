from django.http import HttpResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.db import connection
from django_xhtml2pdf.utils import generate_pdf
from .models import Color

import random


def index(request, sec):
    labels = []
    fecha = ''
    data = ''
    bColor = []
    hColor = []
    lista = []
    meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE",
             "NOVIEMBRE", "DICIEMBRE"]
    dele = []
    # PIE
    with connection.cursor() as cursor:
        if sec == '0':
            cursor.execute(
                "select dl.id_grupo, dl.delito, coalesce(count(*), 0) from mensajes, ctlgo_delito dl cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where d.delito = dl.id_grupo group by dl.delito, dl.id_grupo order by dl.id_grupo")
        else:
            cursor.execute(
                "select dl.id_grupo, dl.delito, coalesce(count(*), 0) from mensajes, ctlgo_delito dl, mapas_lugar cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where d.delito = dl.id_grupo and lower(delegacion) like lower(nombre) and id = %s group by dl.delito, dl.id_grupo order by dl.id_grupo",
                [sec])
        rows = cursor.fetchall()
        max = len(rows)
        listaColores = getRandomColors(max)
        tot = 0
        for row in rows:
            tot = tot + row[2]
        i = 0
        for row in rows:
            labels.append(row[1] + ' - ' + str("%.2f" % (row[2] * (100 / tot))) + '%')
            data = data + str(row[2]) + ', '
            bColor.append(listaColores[i].c1)
            hColor.append(listaColores[i].c2)
            i = i + 1
    # TIME
    with connection.cursor() as cursor:
        if sec == '0':
            cursor.execute(
                "select dl.delito, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '01' and d.delito = dl.id_grupo) as enero, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '02' and d.delito = dl.id_grupo) as febrero, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '03' and d.delito = dl.id_grupo) as marzo, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '04' and d.delito = dl.id_grupo) as abril, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '05' and d.delito = dl.id_grupo) as mayo, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '06' and d.delito = dl.id_grupo) as junio, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '07' and d.delito = dl.id_grupo) as julio, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '08' and d.delito = dl.id_grupo) as agosto, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '09' and d.delito = dl.id_grupo) as septiembre, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '10' and d.delito = dl.id_grupo) as octubre, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '11' and d.delito = dl.id_grupo) as noviembre, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '12' and d.delito = dl.id_grupo) as diciembre from ctlgo_delito dl")
        else:
            cursor.execute(
                "select dl.delito, (select coalesce(count(*), 0) from mensajes, mapas_lugar cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(delegacion) like lower(nombre) and id = %s and to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '01' and d.delito = dl.id_grupo) as enero, (select coalesce(count(*), 0) from mensajes, mapas_lugar cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(delegacion) like lower(nombre) and id = %s and to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '02' and d.delito = dl.id_grupo) as febrero, (select coalesce(count(*), 0) from mensajes, mapas_lugar cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(delegacion) like lower(nombre) and id = %s and to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '03' and d.delito = dl.id_grupo) as marzo, (select coalesce(count(*), 0) from mensajes, mapas_lugar cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(delegacion) like lower(nombre) and id = %s and to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '04' and d.delito = dl.id_grupo) as abril, (select coalesce(count(*), 0) from mensajes, mapas_lugar cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(delegacion) like lower(nombre) and id = %s and to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '05' and d.delito = dl.id_grupo) as mayo, (select coalesce(count(*), 0) from mensajes, mapas_lugar cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(delegacion) like lower(nombre) and id = %s and to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '06' and d.delito = dl.id_grupo) as junio, (select coalesce(count(*), 0) from mensajes, mapas_lugar cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(delegacion) like lower(nombre) and id = %s and to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '07' and d.delito = dl.id_grupo) as julio, (select coalesce(count(*), 0) from mensajes, mapas_lugar cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(delegacion) like lower(nombre) and id = %s and to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '08' and d.delito = dl.id_grupo) as agosto, (select coalesce(count(*), 0) from mensajes, mapas_lugar cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(delegacion) like lower(nombre) and id = %s and to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '09' and d.delito = dl.id_grupo) as septiembre, (select coalesce(count(*), 0) from mensajes, mapas_lugar cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(delegacion) like lower(nombre) and id = %s and to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '10' and d.delito = dl.id_grupo) as octubre, (select coalesce(count(*), 0) from mensajes, mapas_lugar cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(delegacion) like lower(nombre) and id = %s and to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '11' and d.delito = dl.id_grupo) as noviembre, (select coalesce(count(*), 0) from mensajes, mapas_lugar cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(delegacion) like lower(nombre) and id = %s and to_char(fecha, 'YYYY') = '2018' and to_char(fecha, 'MM') = '12' and d.delito = dl.id_grupo) as diciembre from ctlgo_delito dl",
                [sec, sec, sec, sec, sec, sec, sec, sec, sec, sec, sec, sec])
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
    # INFO
    with connection.cursor() as cursor:
        cursor.execute("select max(fecha) from mensajes")
        row = cursor.fetchone()
        fecha = ''.join(row[0].strftime('%d / %m / %Y'))
    # DELEGACIONES
    with connection.cursor() as cursor:
        cursor.execute(
            "select id, nombre, count(*) from mapas_lugar, mensajes where lower(delegacion) like lower(nombre) group by id,nombre order by id")
        rows = cursor.fetchall()
        for row in rows:
            dele.append({'id': row[0], 'nombre': row[1]})

    context = {'labels': labels, 'data': data, 'bColor': bColor, 'hColor': hColor, 'lista': lista, 'meses': meses,
               'fecha': fecha, 'delegaciones': dele, 'sec': sec}
    return render(request, 'reportes/reporte.html', context)


def pdf(request):
    fecha = ''
    lista = []
    cuentas = []
    headers = ["DELITO", "DELEGACION", "LOCALIDAD", "NUMERO INCIDENCIAS"]

    script = "select dl.delito, coalesce(delegacion, '-'), coalesce(localidad, '-'), count(*) as num from mensajes, ctlgo_delito dl cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where dl.id_grupo = d.delito group by dl.delito, delegacion, localidad order by num desc, dl.delito, delegacion, localidad"
    with connection.cursor() as cursor:
        cursor.execute(script)
        rows = cursor.fetchall()
        for row in rows:
            lista.append({'delito': row[0], 'delegacion': row[1], 'localidad': row[2], 'num': row[3]})

    with connection.cursor() as cursor:
        cursor.execute("select max(fecha) from mensajes")
        row = cursor.fetchone()
        fecha = ''.join(row[0].strftime('%d / %m / %Y'))

    with connection.cursor() as cursor:
        cursor.execute("select cuenta from ctlgo_cuentas")
        rows = cursor.fetchall()
        for row in rows:
            cuentas.append({'link': 'https://twitter.com/' + row[0].replace('@', ''), 'nombre': row[0]})

    context = {'headers': headers, 'lista': lista, 'fecha': fecha, 'cuentas': cuentas}

    resp = HttpResponse(content_type='application/pdf')
    result = generate_pdf('reportes/pdf.html', file_object=resp, context=context)
    return result


def getRandomColors(num):
    l = []
    colores = Color.objects.order_by('id')
    ns = random.sample(range(len(colores)), num)
    for n in ns:
        l.append(colores[n])
    return l


def prueba(request):
    fecha = ''
    lista = []
    cuentas = []
    headers = ["DELITO", "DELEGACION", "LOCALIDAD", "NUMERO INCIDENCIAS"]

    script = "select dl.delito, coalesce(delegacion, '-'), coalesce(localidad, '-'), count(*) from mensajes, ctlgo_delito dl cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where dl.id_grupo = d.delito group by dl.delito, delegacion, localidad order by dl.delito, delegacion, localidad"
    with connection.cursor() as cursor:
        cursor.execute(script)
        rows = cursor.fetchall()
        for row in rows:
            lista.append({'delito': row[0], 'delegacion': row[1], 'localidad': row[2], 'num': row[3]})

    with connection.cursor() as cursor:
        cursor.execute("select max(fecha) from mensajes")
        row = cursor.fetchone()
        fecha = ''.join(row[0].strftime('%d / %m / %Y'))

    with connection.cursor() as cursor:
        cursor.execute("select cuenta from ctlgo_cuentas")
        rows = cursor.fetchall()
        for row in rows:
            cuentas.append({'link': 'https://twitter.com/' + row[0].replace('@', ''), 'nombre': row[0]})

    context = {'headers': headers, 'lista': lista, 'fecha': fecha, 'cuentas': cuentas}

    resp = HttpResponse(content_type='application/pdf')
    result = generate_pdf('reportes/prueba.html', file_object=resp, context=context)
    return result
    # return render(request, 'reportes/prueba.html', context)
