# Mapa de los CRA y CRIE de la provincia de Teruel

Web estática (HTML + CSS + JavaScript + Leaflet/OpenStreetMap). Sin registro, sin servidor, sin coste.

## Estructura

| Carpeta / archivo | Para qué sirve |
|---|---|
| `index.html`, `css/`, `js/` | Diseño y funcionamiento. No hace falta tocarlos para cambiar datos. |
| `data/cras.json` | Centros (CRA y CRIE): nombre, sede, localidades, cursos, web, fuente. |
| `data/localidades.json` | Coordenadas de cada localidad. |
| `data/rutas.json` | Trazado real de carreteras (se crea con el script). |
| `data/fotos.json` + `fotos/` | Fotografías de cada centro. |
| `scripts/` | Herramientas para completar coordenadas, rutas y QR. |

## Estado de los datos (léelo antes de publicar)

- 30 centros: 27 CRA y 3 CRIE (Albarracín, Alcorisa y Calamocha). La lista de CRA sale de listados oficiales del Gobierno de Aragón y del Servicio Provincial de Teruel; podría faltar alguno.
- Localidades completas según fuentes: Teruel Uno, Turia, Somontano Bajo Aragón, Muniesa, Albarracín y otros. Varias fuentes tienen años distintos. En 9 CRA solo consta la sede (`"estado": "Solo sede confirmada"`).
- Cursos y servicios: solo hay una definición general (Infantil y Primaria para los CRA). El resto figura como «Pendiente de verificar».
- Coordenadas: solo 1 viene de una fuente oficial. 19 son estimaciones (`"aprox": true`) y el resto están en `null`, por lo que no se dibujan. Corrígelas con el paso 1.
- Fotografías: no se han incluido (no se pueden descargar y reutilizar sin revisar su licencia).

## Paso 1 · Completar coordenadas y carreteras (una vez, con Internet)

Necesitas Python 3 (python.org). Abre una terminal en la carpeta del proyecto:

```
python scripts/actualizar_datos.py geocodificar
python scripts/actualizar_datos.py rutas
```

El primero busca cada pueblo en OpenStreetMap (tarda ~2 min) y avisa de los que debes revisar a mano. El segundo guarda el trazado real de las carreteras en `data/rutas.json`. Repite ambos si añades localidades.
Sin `rutas.json`, la web pide las rutas a OSRM al abrirse y las guarda en el navegador; funciona, pero es más lento y depende de un servicio gratuito externo.

## Paso 2 · Modificar datos

Edita los `.json` con un editor de texto (por ejemplo VS Code) o desde GitHub con el icono del lápiz.
- **Corregir/añadir localidad a un CRA**: en `cras.json`, añade su nombre a `"localidades"`. En `localidades.json` añade `"Nombre": {"lat": null, "lon": null, "aprox": true}` y ejecuta el paso 1.
- **Un campo desconocido**: deja «Pendiente de verificar».
- **Web oficial**: rellena `"web"` con la dirección completa.
- **Fotos**: copia las imágenes en `fotos/<id-del-centro>/` y añade en `data/fotos.json`:
  `{"turia": [{"src": "fotos/turia/fachada.jpg", "pie": "Fachada del CRA Turia"}]}`
- Respeta comas y comillas; si algo falla, valida el archivo en jsonlint.com.

## Paso 3 · Publicar gratis en GitHub Pages

1. Crea una cuenta en github.com y pulsa **New repository** (nombre: `mapa-cra-teruel`, público).
2. **Add file → Upload files**, arrastra todo el contenido de esta carpeta (no la carpeta en sí) y pulsa **Commit changes**.
3. **Settings → Pages → Build and deployment → Deploy from a branch → `main` / `(root)` → Save**.
4. En 1-2 minutos la web estará en `https://TU-USUARIO.github.io/mapa-cra-teruel/`. Esa dirección es pública y permanente mientras no borres el repositorio.

Alternativas gratuitas: Cloudflare Pages o Netlify (arrastrar la carpeta en app.netlify.com/drop).

## Paso 4 · Código QR definitivo

Con la dirección ya activa:

```
pip install "qrcode[pil]"
python scripts/generar_qr.py https://TU-USUARIO.github.io/mapa-cra-teruel/
```

Se crea `qr-mapa-cra-teruel.png`, listo para imprimir. Comprueba que lo lee un móvil antes de imprimir. Si cambias la dirección, el QR dejará de servir; por eso conviene fijar el nombre del repositorio desde el principio.

## Notas técnicas

- Mapa base: mosaicos estándar de OpenStreetMap (uso moderado permitido). Si la web tuviera mucho tráfico, habría que usar un proveedor con plan gratuito propio (p. ej. MapTiler o Stadia Maps).
- Leaflet se carga desde cdnjs. El conjunto pesa menos de 20 KB sin contar mapas ni librería.
- Para probar en local abre una terminal en la carpeta y ejecuta `python -m http.server`; luego visita http://localhost:8000 (abrir `index.html` con doble clic no carga los JSON).
