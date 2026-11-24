'use strict';
// Los datos viven en /data. Este archivo solo dibuja.
const $ = s => document.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const norm = s => String(s).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
const J = async u => { try { const r = await fetch(u); return r.ok ? await r.json() : null; } catch (e) { return null; } };
const PEND = '<em class="pend">Pendiente de verificar</em>';
let C = [], LOC = {}, FOTOS = {}, RUTAS = {}, map, G = {}, M = {}, cache = {};
const S = { q: '', tipo: 'todos', sel: null };
try { cache = JSON.parse(localStorage.getItem('rutasOSRM') || '{}'); } catch (e) {}

const pos = n => { const l = LOC[n]; return l && l.lat != null ? [l.lat, l.lon] : null; };
const icono = (c, sede) => L.divIcon({
  className: '', iconSize: [18, 18], iconAnchor: c.tipo === 'CRIE' ? [0, 22] : [9, 9],
  html: `<span class="pin ${c.tipo === 'CRIE' ? 'crie' : ''} ${sede ? 'sede' : ''}" style="--c:${c.color}"></span>`
});

async function init() {
  [C, LOC, FOTOS, RUTAS] = await Promise.all([J('data/cras.json'), J('data/localidades.json'), J('data/fotos.json'), J('data/rutas.json')]);
  C = C || []; LOC = LOC || {}; FOTOS = FOTOS || {}; RUTAS = RUTAS || {};
  C.forEach((c, i) => c.color = c.tipo === 'CRIE' ? '#111' : `hsl(${Math.round((i * 137.508) % 360)} 62% 40%)`);

  map = L.map('map').setView([40.5, -0.95], 8);
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18, attribution: '© OpenStreetMap' }).addTo(map);
  const lab = () => $('#map').classList.toggle('labels', map.getZoom() >= 10);
  map.on('zoomend', lab); lab();

  const trabajos = [];
  C.forEach(c => {
    G[c.id] = L.layerGroup().addTo(map);
    c.localidades.forEach(n => {
      const p = pos(n); if (!p) return;
      const m = L.marker(p, { icon: icono(c, n === c.sede), title: n }).addTo(G[c.id]);
      m.bindTooltip(n, { permanent: true, direction: 'right', offset: [10, 0], className: 'etq' });
      m.on('click', () => seleccionar(c.id, false));
      (M[c.id] = M[c.id] || {})[n] = m;
      if (c.tipo === 'CRA' && n !== c.sede && pos(c.sede)) trabajos.push([c, n]);
    });
  });
  // Carreteras: siguen el trazado real (rutas.json precalculado, o consulta a OSRM como respaldo).
  (async () => { for (const [c, n] of trabajos) await ruta(c, n); })();

  $('#buscar').addEventListener('input', e => { S.q = e.target.value; pintar(); });
  document.querySelectorAll('.filtros button').forEach(b => b.addEventListener('click', () => {
    S.tipo = b.dataset.t;
    document.querySelectorAll('.filtros button').forEach(x => x.setAttribute('aria-pressed', x === b));
    pintar();
  }));
  pintar(); galeria();
  window.addEventListener('hashchange', vista); vista();
}

async function ruta(c, n) {
  const k = c.id + '|' + n;
  let g = (RUTAS[c.id] || {})[n] || cache[k];
  if (!g) {
    const a = pos(c.sede), b = pos(n);
    const d = await J(`https://router.project-osrm.org/route/v1/driving/${a[1]},${a[0]};${b[1]},${b[0]}?overview=full&geometries=geojson`);
    g = d && d.routes && d.routes[0] && d.routes[0].geometry.coordinates;
    if (!g) return;
    cache[k] = g;
    try { localStorage.setItem('rutasOSRM', JSON.stringify(cache)); } catch (e) {}
    await new Promise(r => setTimeout(r, 400));
  }
  L.polyline(g.map(p => [p[1], p[0]]), { color: c.color, weight: 4, opacity: .85 }).addTo(G[c.id]);
}

const visible = c => {
  const q = norm(S.q.trim());
  return (S.tipo === 'todos' || c.tipo === S.tipo) &&
    (!q || norm([c.nombre, c.sede, ...c.localidades].join(' ')).includes(q));
};

function pintar() {
  const v = C.filter(visible);
  $('#lista').innerHTML = v.length ? v.map(c => `<li tabindex="0" data-id="${c.id}" class="${S.sel === c.id ? 'sel' : ''}">
    <span class="pin ${c.tipo === 'CRIE' ? 'crie' : ''}" style="--c:${c.color}"></span>
    <span><strong>${esc(c.nombre)}</strong><small>Sede: ${esc(c.sede)} · ${c.localidades.length} localidad${c.localidades.length > 1 ? 'es' : ''}</small></span></li>`).join('')
    : '<li>Sin resultados</li>';
  document.querySelectorAll('#lista li[data-id]').forEach(li => {
    li.addEventListener('click', () => seleccionar(li.dataset.id, true));
    li.addEventListener('keydown', e => { if (e.key === 'Enter') seleccionar(li.dataset.id, true); });
  });
  C.forEach(c => visible(c) ? map.addLayer(G[c.id]) : map.removeLayer(G[c.id]));
}

function seleccionar(id, ajustar) {
  const c = C.find(x => x.id === id); if (!c) return;
  S.sel = id; pintar();
  const pts = c.localidades.map(pos).filter(Boolean);
  if (ajustar && pts.length) pts.length > 1 ? map.fitBounds(pts, { padding: [60, 60], maxZoom: 12 }) : map.setView(pts[0], 11);
  ficha(c);
}

function ficha(c) {
  const f = $('#ficha');
  const fotos = FOTOS[c.id] || [];
  const chips = c.localidades.map(n => {
    const p = pos(n), ap = LOC[n] && LOC[n].aprox;
    return p ? `<button data-n="${esc(n)}" style="--c:${c.color}" title="${ap ? 'Coordenadas aproximadas' : ''}">${esc(n)}${ap ? ' ~' : ''}</button>`
             : `<button class="sin" disabled title="Sin coordenadas todavía">${esc(n)} (sin ubicar)</button>`;
  }).join('');
  f.innerHTML = `<button class="x" aria-label="Cerrar ficha">×</button>
    <h2>${esc(c.nombre)}</h2><p><span class="pin ${c.tipo === 'CRIE' ? 'crie' : ''}" style="--c:${c.color}"></span> ${c.tipo === 'CRIE' ? 'Centro Rural de Innovación Educativa' : 'Colegio Rural Agrupado'}</p>
    <dl>
     <dt>Sede</dt><dd>${esc(c.sede)}</dd>
     <dt>Localidades</dt><dd class="chips">${chips}</dd>
     <dt>Cursos</dt><dd>${esc(c.cursos) || PEND}</dd>
     <dt>Servicios educativos</dt><dd>${c.servicios && c.servicios !== 'Pendiente de verificar' ? esc(c.servicios) : PEND}</dd>
     <dt>Información general</dt><dd>${esc(c.info) || PEND}</dd>
     <dt>Estado de los datos</dt><dd>${esc(c.estado) || PEND}</dd>
    </dl>
    ${c.web ? `<a class="btn" href="${esc(c.web)}" target="_blank" rel="noopener">Web oficial</a>` : '<p class="pend">Web oficial: pendiente de verificar</p>'}
    <details ${fotos.length ? 'open' : ''}><summary>Fotografías (${fotos.length})</summary>
      ${fotos.length ? `<div class="fotos">${fotos.map(x => `<img loading="lazy" src="${esc(x.src)}" alt="${esc(x.pie || c.nombre)}">`).join('')}</div>` : '<p>Aún no hay fotografías. Se añaden en <code>fotos/</code> y <code>data/fotos.json</code>.</p>'}
    </details>
    ${c.fuente ? `<p><small>Fuente: <a href="${esc(c.fuente)}" target="_blank" rel="noopener">enlace</a></small></p>` : ''}`;
  f.hidden = false;
  f.querySelector('.x').onclick = () => { f.hidden = true; S.sel = null; pintar(); };
  f.querySelectorAll('.chips button[data-n]').forEach(b => b.onclick = () => {
    const m = (M[c.id] || {})[b.dataset.n]; if (m) { map.flyTo(m.getLatLng(), 12); m.openTooltip(); }
  });
}

function galeria() {
  const g = C.filter(c => (FOTOS[c.id] || []).length);
  $('#galeria').innerHTML = g.length ? g.map(c => `<h3>${esc(c.nombre)}</h3><div class="fotos">${FOTOS[c.id].map(x => `<figure><img loading="lazy" src="${esc(x.src)}" alt="${esc(x.pie || c.nombre)}"><figcaption><small>${esc(x.pie || '')}</small></figcaption></figure>`).join('')}</div>`).join('')
    : '<p>Todavía no hay fotografías. Para añadirlas, copia las imágenes en <code>fotos/</code> y descríbelas en <code>data/fotos.json</code> (ver README).</p>';
}

function vista() {
  const v = (location.hash || '#mapa').slice(1);
  ['mapa', 'info', 'fotos'].forEach(n => $('#v-' + n).hidden = n !== v);
  document.querySelectorAll('nav a').forEach(a => a.classList.toggle('on', a.dataset.v === v));
  if (v === 'mapa') setTimeout(() => map.invalidateSize(), 50);
}
init();
