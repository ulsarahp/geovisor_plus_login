// ================================================================
// CONFIG — única definición de constantes
// Modo local: carga capas desde assets/data/*.geojson
// Modo GeoServer: carga desde WFS remoto
// Para cambiar: usar ?geoserver=... o dejar el fallback local
// ================================================================

function resolveGeoserverBase(){
  try{
    var q = null;
    try{ q = new URLSearchParams(location.search).get('geoserver'); }catch(e){}
    if(q){
      try{ localStorage.setItem('geovisor-geoserver', q); }catch(e){}
      return q;
    }
    try{
      var saved = localStorage.getItem('geovisor-geoserver');
      if(saved && saved !== 'local') return saved;
    }catch(e){}
  }catch(e){}
  var h = '';
  try{ h = location.hostname || ''; }catch(e){}
  if(h==='localhost' || h==='127.0.0.1' || h===''){
    return 'http://localhost:8081/geoserver/SIG-DES/wfs?';
  }
  return 'https://geoserver.conanp.gob.mx/geoserver/SIG-DES/wfs?';
}

var GEOSERVER_BASE = resolveGeoserverBase();
var WORKSPACE = 'SIG-DES';
var CAPAS_CONOCIDAS = ['shp_advc','shp_anp','shp_kba_mex','shp_ramsar','shp_ramsar_mex','shp_reg_conanp','shp_reg_conanp_mex','shp_unescomab_mex','shp_unescopatrimonio_mex','shp_zp_anp_mex','shp_00ent','shp_00mun'];
var NOMBRES_ESPECIALES = {'shp_00ent':'Límite estatal','shp_00mun':'Límite municipal','shp_ramsar':'Sitios RAMSAR México','shp_unescomab_mex':'UNESCO MaB'};
var SHAPE_URLS = {
  'shp_advc': 'https://sig.conanp.gob.mx/container/descargas/files/shape/623_ADVC_VIGENTES_JUNIO_2026.zip',
  'shp_anp': 'https://sig.conanp.gob.mx/container/descargas/files/shape/232-ANP_ITRF08_19162026.zip'
};

// MODO LOCAL: carga GeoJSON desde assets/data
// Si el archivo existe localmente, se usa; si no, cae a WFS
var MODO_LOCAL = true; // true = intentar local primero

try{
  window.GEOSERVER_BASE = GEOSERVER_BASE;
  window.WORKSPACE = WORKSPACE;
  window.CAPAS_CONOCIDAS = CAPAS_CONOCIDAS;
  window.NOMBRES_ESPECIALES = NOMBRES_ESPECIALES;
  window.SHAPE_URLS = SHAPE_URLS;
  window.resolveGeoserverBase = resolveGeoserverBase;
  window.MODO_LOCAL = MODO_LOCAL;
}catch(e){}

// Exportación para main.js (módulo ES)
