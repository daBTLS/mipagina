from django.shortcuts import render
from django.db import connection
from .models import Lugar, Color


def index(request):
    max = 0
    lista = []
    colores = Color.objects.order_by('id')
    script = "select id, nombre, coordenadas, (select coalesce(sum(indice_delito), 0) from mensajes where lower(delegacion) like lower(nombre)) as sum, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(delegacion) like lower(nombre) and d.delito = 1) as asesinato, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(delegacion) like lower(nombre) and d.delito = 2) as secuestro, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(delegacion) like lower(nombre) and d.delito = 3) as violacion, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(delegacion) like lower(nombre) and d.delito = 4) as robo_privado, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(delegacion) like lower(nombre) and d.delito = 5) as robo_negocio, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(delegacion) like lower(nombre) and d.delito = 6) as fraude, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(delegacion) like lower(nombre) and d.delito = 7) as robo_transporte from mapas_lugar order by sum"
    sc = "select delegacion, sum(indice_delito) as total from mensajes where delegacion is not null group by delegacion order by total"
    with connection.cursor() as cursor:
        cursor.execute(sc)
        rw = cursor.fetchall()
        max = rw[len(rw) - 1][1]

    with connection.cursor() as cursor:
        cursor.execute(script)
        for row in cursor.fetchall():
            lista.append({'id': row[0], 'nombre': row[1], 'coordenadas': row[2],
                          'color': colores[len(colores) - 1].codigo if row[3] == 0 else asignaColor(colores, max,
                                                                                                    row[3]),
                          'asesinato': row[4], 'secuestro': row[5], 'violacion': row[6], 'robo_privado': row[7],
                          'robo_negocio': row[8], 'fraude': row[9], 'robo_transporte': row[10]})
    cen = '{lat: 19.32055625, lng: -99.1517010707765}'
    context = {'lista': lista, 'cen': cen}
    return render(request, 'mapas/mapa.html', context)


def detalle(request, sec):
    max = 0
    lista = []
    colores = Color.objects.order_by('id')
    with connection.cursor() as cursor:
        cursor.execute(
            "select localidad, sum(indice_delito) as total from mensajes, zonas_tmp, mapas_lugar m where lower(mun_name) like lower(nombre) and lower(localidad) like lower(sett_name) and localidad is not null and st_name like '%%DISTRITO%%' and m.id = %s group by localidad order by total",
            [sec])
        rw = cursor.fetchall()
        max = rw[len(rw) - 1][1]
    with connection.cursor() as cursor:
        cursor.execute(
            "select z.id, z.sett_name, ST_AsGeoJson(geom) AS geojson, (select coalesce(sum(indice_delito), 0) from mensajes where lower(localidad) like lower(z.sett_name)) as sum, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(localidad) like lower(z.sett_name) and d.delito = 1) as asesinato, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(localidad) like lower(z.sett_name) and d.delito = 2) as secuestro, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(localidad) like lower(z.sett_name) and d.delito = 3) as violacion, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(localidad) like lower(z.sett_name) and d.delito = 4) as robo_privado, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(localidad) like lower(z.sett_name) and d.delito = 5) as robo_negocio, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(localidad) like lower(z.sett_name) and d.delito = 6) as fraude, (select coalesce(count(*), 0) from mensajes cross join lateral unnest(array[delito1, delito2, delito3]) with ordinality as d (delito, i) where lower(localidad) like lower(z.sett_name) and d.delito = 7) from zonas_tmp z, mapas_lugar m where lower(z.mun_name) like lower(m.nombre) and z.st_name like '%%DISTRITO%%' and m.id = %s",
            [sec])

        for row in cursor.fetchall():
            res = ''.join(row[2]).replace("{\"type\":\"MultiPolygon\",\"coordinates\":[[[", "")
            res = res.replace(",0]]]]}", "}")
            res = res.replace("[", "{lng: ")
            res = res.replace(",0],", "}_\n")
            res = res.replace(",", ", lat: ")
            res = res.replace("_", ",")
            rs = res.split(', lat: 0]], lat:', 1)
            if len(rs) != 1:
                res = rs[0] + '}'
            lista.append({'id': row[0], 'nombre': row[1], 'coordenadas': res,
                          'color': colores[len(colores) - 1].codigo if row[3] == 0 else asignaColor(colores, max,
                                                                                                    row[3]),
                          'asesinato': row[4], 'secuestro': row[5], 'violacion': row[6], 'robo_privado': row[7],
                          'robo_negocio': row[8], 'fraude': row[9], 'robo_transporte': row[10]})
        l = Lugar.objects.raw('select * from mapas_lugar where id = %s', [sec])[0]
        cen = l.centro
    context = {'lista': lista, 'cen': cen}
    return render(request, 'mapas/detalle.html', context)


def prueba(request):
    # COORDENADAS DE ARCHIVO
    # module_dir = os.path.dirname(__file__)
    # file_path = os.path.join(module_dir, 'static\coordenadas.txt')
    # f = open(file_path, 'r')
    # file_content = f.read()
    # f.close()

    # COORDENADAS DE CONSULTA DIRECTA
    # with connection.cursor() as cursor:
    # cursor.execute(
    #     "select ST_AsGeoJson(geom) AS geojson from zonas_tmp where postalcode = %s",
    #     ['06200'])
    # row = cursor.fetchone()
    #
    # res = ''.join(row).replace("{\"type\":\"MultiPolygon\",\"coordinates\":[[[", "")
    # res = res.replace(",0]]]]}", "}")
    # res = res.replace("[", "{lng: ")
    # res = res.replace(",0],", "}-\n")
    # res = res.replace(",", ", lat: ")
    # res = res.replace("-", ",")
    # cen = res.split(",\n{")[0]

    with connection.cursor() as cursor:
        cursor.execute(
            "select ST_AsGeoJson(geom) AS geojson from zonas_tmp where postalcode = %s;",
            ['06010'])
        row = cursor.fetchone()

        res = ''.join(row).replace("{\"type\":\"MultiPolygon\",\"coordinates\":[[[", "")
        res = res.replace(",0]]]]}", "}")
        res = res.replace("[", "{lng: ")
        res = res.replace(",0],", "}_\n")
        res = res.replace(",", ", lat: ")
        res = res.replace("_", ",")

        cen = res.split(",\n{")[0]

        # CONSULTA NATIVA
        l = Lugar.objects.raw('select * from mapas_lugar order by id')[4]
        res = l.coordenadas
        cen = l.centro

    context = {'coordenadas': res, 'cen': cen}
    return render(request, 'mapas/prueba.html', context)


def asignaColor(colores, max, val):
    c = colores[len(colores) - 2].codigo
    inc = max / (len(colores) - 1)
    for x in range(len(colores) - 1):
        if val <= (inc * x):
            c = colores[x - 1].codigo
            return c
    return c
