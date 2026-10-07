import pathlib, re

W = pathlib.Path("D:/CONP/GITHUB/geovisor_plus_login".replace("CONP","CONANP"))
p = W/"assets"/"js"/"app.js"
t = p.read_text(encoding="utf-8")

# Reemplazar fetchWFSGeoJSON para soportar modo local
old_fetch = "async function fetchWFSGeoJSON(typeName){try{const resp=await fetch(`${GEOSERVER_BASE}service=WFS&version=1.1.0&request=GetFeature&typeName=${WORKSPACE}:${typeName}&outputFormat=application/json`);if(!resp.ok)return[];const text=await resp.text();let g;try{g=JSON.parse(text);}catch(e){return[];}if(g.type==='FeatureCollection')return g.features.map(f=>({type:'Feature',geometry:f.geometry,properties:f.properties}));return[];}catch(e){return[];}}"

new_fetch = """async function fetchWFSGeoJSON(typeName){
  // MODO LOCAL: intentar cargar desde assets/data primero
  if(typeof MODO_LOCAL !== 'undefined' && MODO_LOCAL){
    try{
      const r = await fetch('assets/data/' + typeName + '.geojson');
      if(r.ok){
        const g = await r.json();
        if(g.type === 'FeatureCollection' && g.features && g.features.length > 0){
          console.log('[WFS] ' + typeName + ' cargada desde archivo local (' + g.features.length + ' features)');
          return g.features;
        }
      }
    }catch(e){ console.warn('[WFS] ' + typeName + ' no disponible local, probando GeoServer...'); }
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

if old_fetch in t:
    t = t.replace(old_fetch, new_fetch, 1)
    print("fetchWFSGeoJSON updated with local mode support")
else:
    # Try more flexible
    pat = re.compile(r'async function fetchWFSGeoJSON\(typeName\)\{.*?\n\}', re.DOTALL)
    m = pat.search(t)
    if m:
        t = pat.sub(lambda m: new_fetch, t, count=1)
        print("fetchWFSGeoJSON replaced via regex")
    else:
        print("fetchWFSGeoJSON NOT FOUND")

# Also update getCapasDesdeWFS to check local files too
old_check = "async function getCapasDesdeWFS()"
if old_check in t:
    print("getCapasDesdeWFS found - updating...")
    # Find the function and add local check at the beginning
    idx = t.find(old_check)
    # Find the function body opening
    brace = t.find("{", idx)
    # Insert local check right after the opening brace
    local_check = """
  // MODO LOCAL: verificar archivos disponibles en assets/data
  if(typeof MODO_LOCAL !== 'undefined' && MODO_LOCAL){
    const disponibles = [];
    for(const nombre of CAPAS_CONOCIDAS){
      try{
        const r = await fetch('assets/data/' + nombre + '.geojson', {method:'HEAD'});
        if(r.ok){ disponibles.push(nombre); continue; }
      }catch(e){}
      // Fallback: probar GeoServer
      try{
        const url = `${GEOSERVER_BASE}service=WFS&version=1.1.0&request=GetFeature&typeName=${WORKSPACE}:${nombre}&outputFormat=application/json&maxFeatures=1`;
        const resp = await fetch(url);
        if(resp.ok){
          const text = await resp.text();
          try{
            const json = JSON.parse(text);
            if(json.type === 'FeatureCollection') disponibles.push(nombre);
          }catch(e){}
        }
      }catch(e){}
    }
    return disponibles;
  }
"""
    t = t[:brace+1] + local_check + t[brace+1:]
    print("getCapasDesdeWFS updated with local check")

p.write_text(t, encoding="utf-8")
print(f"app.js: {len(t)}")
