import pathlib

W = pathlib.Path("D:/CONANP/GITHUB/geovisor_plus_login")
p = W/"assets"/"js"/"app.js"
t = p.read_text(encoding="utf-8")

# Encontrar la función exacta por string matching (no regex)
func_name = "async function fetchWFSGeoJSON(typeName){"
idx = t.find(func_name)
assert idx >= 0, "fetchWFSGeoJSON not found"

# Encontrar el final con balanced braces
depth = 0
end = idx
for i in range(idx, len(t)):
    if t[i] == '{':
        depth += 1
    elif t[i] == '}':
        depth -= 1
        if depth == 0:
            end = i + 1
            break

old_func = t[idx:end]
print(f"Old function: {len(old_func)} chars")

new_func = """async function fetchWFSGeoJSON(typeName){
  // MODO LOCAL: intentar cargar desde assets/data primero
  if(typeof MODO_LOCAL !== 'undefined' && MODO_LOCAL){
    try{
      const r = await fetch('assets/data/' + typeName + '.geojson');
      if(r.ok){
        const g = await r.json();
        if(g.type === 'FeatureCollection' && g.features && g.features.length > 0){
          console.log('[WFS] ' + typeName + ' local (' + g.features.length + ' features)');
          return g.features;
        }
      }
    }catch(e){ console.warn('[WFS] ' + typeName + ' no local, probando GeoServer'); }
  }
  // MODO GEOSERVER: fallback a WFS remoto
  try{
    const resp = await fetch(`${GEOSERVER_BASE}service=WFS&version=1.1.0&request=GetFeature&typeName=${WORKSPACE}:${typeName}&outputFormat=application/json`);
    if(!resp.ok) return [];
    const text = await resp.text();
    let g;
    try{ g = JSON.parse(text); }catch(e){ return []; }
    if(g.type === 'FeatureCollection') return g.features.map(f => ({type:'Feature', geometry:f.geometry, properties:f.properties}));
    return [];
  }catch(e){ return []; }
}"""

t = t[:idx] + new_func + t[end:]
print(f"Replaced fetchWFSGeoJSON: {len(old_func)} -> {len(new_func)}")

# Actualizar getCapasDesdeWFS: añadir chequeo local al principio
old_check_start = "async function getCapasDesdeWFS(){"
check_idx = t.find(old_check_start)
if check_idx >= 0:
    brace_pos = t.find("{", check_idx + len("async function getCapasDesdeWFS()"))
    local_check = """
  // MODO LOCAL: verificar archivos en assets/data antes de consultar GeoServer
  if(typeof MODO_LOCAL !== 'undefined' && MODO_LOCAL){
    const locales = [];
    for(const nombre of CAPAS_CONOCIDAS){
      try{
        const r = await fetch('assets/data/' + nombre + '.geojson', {method:'HEAD'});
        if(r.ok){ locales.push(nombre); continue; }
      }catch(e){}
      try{
        const url = `${GEOSERVER_BASE}service=WFS&version=1.1.0&request=GetFeature&typeName=${WORKSPACE}:${nombre}&outputFormat=application/json&maxFeatures=1`;
        const resp = await fetch(url);
        if(resp.ok){
          const text = await resp.text();
          try{
            const json = JSON.parse(text);
            if(json.type === 'FeatureCollection') locales.push(nombre);
          }catch(e){}
        }
      }catch(e){}
    }
    if(locales.length > 0){
      console.log('[WFS] ' + locales.length + ' capas disponibles (' + 'local + geoserver)');
      return locales;
    }
  }
"""
    t = t[:brace_pos+1] + local_check + t[brace_pos+1:]
    print("getCapasDesdeWFS updated with local check")

p.write_text(t, encoding="utf-8")
print(f"app.js: {len(t)}")
