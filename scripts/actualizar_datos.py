"""Herramientas de datos (solo Python 3, sin instalar nada). Necesita Internet.
  python scripts/actualizar_datos.py geocodificar   -> corrige data/localidades.json con OpenStreetMap (Nominatim)
  python scripts/actualizar_datos.py rutas          -> crea data/rutas.json con el trazado real de las carreteras (OSRM)
Ejecutar desde la carpeta principal del proyecto."""
import json, sys, time, urllib.parse, urllib.request
UA = {'User-Agent': 'mapa-cra-teruel/1.0 (proyecto educativo)'}
def get(u):
    with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40) as r:
        return json.load(r)
def cargar(f): return json.load(open(f, encoding='utf-8'))
def guardar(f, d): json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

def geocodificar():
    loc = cargar('data/localidades.json')
    for n, v in loc.items():
        q = urllib.parse.urlencode({'q': f"{v.get('buscar', n)}, Teruel, España", 'format': 'json', 'limit': 3, 'countrycodes': 'es'})
        r = [x for x in get('https://nominatim.openstreetmap.org/search?' + q) if 'Teruel' in x['display_name']]
        if r:
            lat, lon = round(float(r[0]['lat']), 5), round(float(r[0]['lon']), 5)
            if v.get('lat') is not None and abs(lat - v['lat']) + abs(lon - v['lon']) > 0.05:
                print('REVISAR (cambio grande):', n, v['lat'], v['lon'], '->', lat, lon)
            v.update(lat=lat, lon=lon, aprox=False)
            print('ok', n, lat, lon)
        else:
            print('SIN RESULTADO (rellenar a mano):', n)
        time.sleep(1.2)  # norma de uso de Nominatim: 1 petición por segundo
    guardar('data/localidades.json', loc)

def rutas():
    loc, cras, out = cargar('data/localidades.json'), cargar('data/cras.json'), {}
    p = lambda n: (loc.get(n) or {}).get('lat') is not None
    for c in cras:
        if c['tipo'] != 'CRA' or not p(c['sede']): continue
        a = loc[c['sede']]
        for n in c['localidades']:
            if n == c['sede'] or not p(n): continue
            b = loc[n]
            u = f"https://router.project-osrm.org/route/v1/driving/{a['lon']},{a['lat']};{b['lon']},{b['lat']}?overview=full&geometries=geojson"
            try:
                out.setdefault(c['id'], {})[n] = get(u)['routes'][0]['geometry']['coordinates']
                print('ok', c['nombre'], n)
            except Exception as e:
                print('FALLO', c['nombre'], n, e)
            time.sleep(0.5)
    guardar('data/rutas.json', out)

if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] in ('geocodificar', 'rutas'):
    {'geocodificar': geocodificar, 'rutas': rutas}[sys.argv[1]]()
else:
    print(__doc__)
