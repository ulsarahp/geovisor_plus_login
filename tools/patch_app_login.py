import pathlib, re

W = pathlib.Path("D:/CONANP/GITHUB/geovisor_plus_login")
p = W/"assets"/"js"/"app.js"
t = p.read_text(encoding="utf-8")

# ================================================================
# Añadir manejo de secciones estratégicas en switchTab
# ================================================================
# Buscar el cierre del else-if de huracanes
hur_end = t.find("tabId==='huracanes'")
if hur_end >= 0:
    # Buscar el cierre de ese bloque (el siguiente "if(tabId!=='dashboard')")
    # o el siguiente "else if" que ya no exista
    close_pat = re.compile(r"(tabId==='huracanes'.*?gCount\.style\.display='none';)", re.DOTALL)
    m = close_pat.search(t)
    if m:
        new_sections = m.group(1) + """
  else if(tabId==='trenes'){
    var trPanel=document.getElementById('seccion-trenes');
    if(trPanel) trPanel.classList.add('visible');
    ['seccion-polos','seccion-subsidios','seccion-selvamaya','seccion-incendios','seccion-huracanes'].forEach(function(id){var e=document.getElementById(id);if(e)e.classList.remove('visible');});
    var cl3=document.getElementById('capa-list'); if(cl3){cl3.style.display='none';cl3.style.flex='0 0 auto';}
    gCount.style.display='none'; gArea.style.display='none'; gAdvc.style.display='none';
    console.log('[Tab] Trenes activado');
  }
  else if(tabId==='polos'){
    var poPanel=document.getElementById('seccion-polos');
    if(poPanel) poPanel.classList.add('visible');
    ['seccion-trenes','seccion-subsidios','seccion-selvamaya','seccion-incendios','seccion-huracanes'].forEach(function(id){var e=document.getElementById(id);if(e)e.classList.remove('visible');});
    var cl4=document.getElementById('capa-list'); if(cl4){cl4.style.display='none';cl4.style.flex='0 0 auto';}
    gCount.style.display='none'; gArea.style.display='none'; gAdvc.style.display='none';
    console.log('[Tab] Polos activado');
  }
  else if(tabId==='subsidios'){
    var suPanel=document.getElementById('seccion-subsidios');
    if(suPanel) suPanel.classList.add('visible');
    ['seccion-trenes','seccion-polos','seccion-selvamaya','seccion-incendios','seccion-huracanes'].forEach(function(id){var e=document.getElementById(id);if(e)e.classList.remove('visible');});
    var cl5=document.getElementById('capa-list'); if(cl5){cl5.style.display='none';cl5.style.flex='0 0 auto';}
    gCount.style.display='none'; gArea.style.display='none'; gAdvc.style.display='none';
    console.log('[Tab] Subsidios activado');
  }
  else if(tabId==='selvamaya'){
    var smPanel=document.getElementById('seccion-selvamaya');
    if(smPanel) smPanel.classList.add('visible');
    ['seccion-trenes','seccion-polos','seccion-subsidios','seccion-incendios','seccion-huracanes'].forEach(function(id){var e=document.getElementById(id);if(e)e.classList.remove('visible');});
    var cl6=document.getElementById('capa-list'); if(cl6){cl6.style.display='none';cl6.style.flex='0 0 auto';}
    gCount.style.display='none'; gArea.style.display='none'; gAdvc.style.display='none';
    console.log('[Tab] Selva Maya activado');
  }"""
        t = t[:m.start(1)] + new_sections + t[m.end(1):]
        print("Strategic sections added to switchTab")
    else:
        print("Could not find huracanes block end")
else:
    print("huracanes tab not found in switchTab")

# ================================================================
# Actualizar el cleanup para incluir secciones estratégicas
# ================================================================
old_cleanup = "if(tabId!=='incendios'&&typeof limpiarIncendios==='function')limpiarIncendios();if(tabId!=='huracanes'&&typeof limpiarHuracanes==='function')limpiarHuracanes();"
new_cleanup = """if(tabId!=='incendios'&&typeof limpiarIncendios==='function')limpiarIncendios();if(tabId!=='huracanes'&&typeof limpiarHuracanes==='function')limpiarHuracanes();
  ['seccion-trenes','seccion-polos','seccion-subsidios','seccion-selvamaya'].forEach(function(id){ if(tabId!=='trenes'&&tabId!=='polos'&&tabId!=='subsidios'&&tabId!=='selvamaya'){ var e=document.getElementById(id);if(e)e.classList.remove('visible'); } });"""

if old_cleanup in t:
    t = t.replace(old_cleanup, new_cleanup, 1)
    print("Cleanup updated for strategic sections")

# ================================================================
# Añadir switchSubtema function
# ================================================================
subtema_func = """
// Dashboard sub-temas estratégicos (solo con login)
var subtemaActual = null;
function switchSubtema(subtema) {
  if (!window.isLoggedIn || !window.isLoggedIn()) {
    console.warn('[Dashboard] Login requerido para sub-temas');
    window.showLoginModal();
    return;
  }
  subtemaActual = subtema;
  console.log('[Dashboard] Subtema:', subtema);
  // Actualizar botones
  document.querySelectorAll('#dashboard-subtemas button').forEach(function(b) {
    b.classList.toggle('active', b.dataset.subtema === subtema);
  });
  // Aquí se cargarán los datos específicos de cada subtema cuando estén listos
  var msg = {
    'trenes': 'Dashboard Trenes: corredores ferroviarios vs ANP (en construcción)',
    'polos': 'Dashboard Polos del Bienestar: polos vs ANP (en construcción)',
    'subsidios': 'Dashboard Subsidios: distribución por ANP (en construcción)',
    'selvamaya': 'Dashboard Selva Maya: monitoreo (en construcción)'
  };
  console.log(msg[subtema] || 'Subtema: ' + subtema);
}
window.switchSubtema = switchSubtema;
"""

if "function switchSubtema" not in t:
    t += "\n" + subtema_func
    print("switchSubtema added")

# ================================================================
# Ocultar/mostrar pestañas según login en el switchTab
# ================================================================
if "SECCIONES_ESTRATEGICAS" not in t:
    # Añadir check en switchTab: si la pestaña es estratégica y no hay login, mostrar modal
    guard = """
  // Guard: sección estratégica requiere login
  if(typeof SECCIONES_ESTRATEGICAS !== 'undefined' && SECCIONES_ESTRATEGICAS.includes(tabId)){
    if(typeof window.isLoggedIn === 'function' && !window.isLoggedIn()){
      console.warn('[Tab] Acceso denegado a:', tabId);
      if(typeof window.showLoginModal === 'function') window.showLoginModal();
      return;
    }
  }
"""
    # Insertar al principio del switchTab
    switch_idx = t.find("function switchTab(tabId){")
    if switch_idx >= 0:
        # Encontrar la primera línea después del {
        brace_end = t.find("{", switch_idx) + 1
        t = t[:brace_end] + "\n" + guard + t[brace_end:]
        print("Login guard added to switchTab")

p.write_text(t, encoding="utf-8")
print(f"app.js: {len(t)}")
