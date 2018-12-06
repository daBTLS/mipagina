from django.shortcuts import render
from django.db import connection


def index(request):
    return render(request, 'index.html')


def info(request):
    cuentas = []
    with connection.cursor() as cursor:
        cursor.execute("select cuenta from ctlgo_cuentas")
        rows = cursor.fetchall()
        for row in rows:
            cuentas.append({'link': 'https://twitter.com/' + row[0].replace('@', ''), 'nombre': row[0]})

    context = {'cuentas': cuentas}
    return render(request, 'info.html', context)
