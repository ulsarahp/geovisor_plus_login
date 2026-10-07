import pathlib, re

W = pathlib.Path("D:/CONANP/GITHUB/geovisor_plus_login")
p = W/"assets"/"js"/"app.js"
t = p.read_text(encoding="utf-8")

# 1. Encontrar el final del bloque huracanes (gAdvc...} al final del else-if)
pat = re.compile(r"else if\(tabId==='huracanes'\)\{.*?gAdvc\.style\.display='none';\s*\}", re.DOTALL)
m = pat.search(t)
if not m:
    # Alternative: find the huracanes block differently
    i = t.find("tabId==='huracanes'")
    if i >= 0:
        j = t.find("gAdvc.style.display='none'", i)
        if j >= 0:
            k = t.find("}", j)
            print(f"huracanes block: start={i}, gAdvc={j}, close_brace={k}")
            # Insert after close brace
            insert_pos = k + 1
            new_code = """
  else if(tabId==='trenes'){
    var trPanel=document.getElementById('seccion-trenes');
    if(trPanel) trPanel.classList.add('visible');
    ['seccion-polos','seccion-subsidios','seccion-selvamaya','seccion-incendios','seccion-huracanes'].forEach(function(id){var e=document.getElementById(id);if(e)e.classList.remove('visible');});
    var cl3=document.getElementById('capa-list'); if(cl3){cl3.style.display='none';cl3.style.flex='0 0 auto';}
    gCount.style.display='none'; gArea.style.display='none'; gAdvc.style.display='none';
  }
  else if(tabId==='polos'){
    var poPanel=document.getElementById('seccion-polos');
    if(poPanel) poPanel.classList.add('visible');
    ['seccion-trenes','seccion-subsidios','seccion-selvamaya','seccion-incendios','seccion-huracanes'].forEach(function(id){var e=document.getElementById(id);if(e)e.classList.remove('visible');});
    var cl4=document.getElementById('capa-list'); if(cl4){cl4.style.display='none';cl4.style.flex='0 0 auto';}
    gCount.style.display='none'; gArea.style.display='none'; gAdvc.style.display='none';
  }
  else if(tabId==='subsidios'){
    var suPanel=document.getElementById('seccion-subsidios');
    if(suPanel) suPanel.classList.add('visible');
    ['seccion-trenes','seccion-polos','seccion-selvamaya','seccion-incendios','seccion-huracanes'].forEach(function(id){var e=document.getElementById(id);if(e)e.classList.remove('visible');});
    var cl5=document.getElementById('capa-list'); if(cl5){cl5.style.display='none';cl5.style.flex='0 0 auto';}
    gCount.style.display='none'; gArea.style.display='none'; gAdvc.style.display='none';
  }
  else if(tabId==='selvamaya'){
    var smPanel=document.getElementById('seccion-selvamaya');
    if(smPanel) smPanel.classList.add('visible');
    ['seccion-trenes','seccion-polos','seccion-subsidios','seccion-incendios','seccion-huracanes'].forEach(function(id){var e=document.getElementById(id);if(e)e.classList.remove('visible');});
    var cl6=document.getElementById('capa-list'); if(cl6){cl6.style.display='none';cl6.style.flex='0 0 auto';}
    gCount.style.display='none'; gArea.style.display='none'; gAdvc.style.display='none';
  }"""
            t = t[:insert_pos] + new_code + t[insert_pos:]
            p.write_text(t, encoding="utf-8")
            print(f"Strategic sections inserted at position {insert_pos}")
            print(f"app.js: {len(t)}")
    else:
        print("gAdvc not found after huracanes")
else:
    insert_pos = m.end()
    print(f"Found pattern, inserting at {insert_pos}")
    # ... same insertion code

# 2. Add switchSubtema
if "function switchSubtema" not in t:
    t += """
// Dashboard sub-temas estratégicos (solo con login)
function switchSubtema(subtema) {
  if (typeof window.isLoggedIn === 'function' && !window.isLoggedIn()) {
    if (typeof window.showLoginModal === 'function') window.showLoginModal();
    return;
  }
  document.querySelectorAll('#dashboard-subtemas button').forEach(function(b) {
    b.classList.toggle('active', b.dataset.subtema === subtema);
  });
  console.log('[Dashboard] Subtema:', subtema);
}
window.switchSubtema = switchSubtema;
"""
    print("switchSubtema added")

# 3. Add login guard at top of switchTab
if "SECCIONES_ESTRATEGICAS" not in t:
    guard = """
  if(typeof SECCIONES_ESTRATEGICAS !== 'undefined' && SECCIONES_ESTRATEGICAS.includes(tabId)){
    if(typeof window.isLoggedIn === 'function' && !window.isLoggedIn()){
      if(typeof window.showLoginModal === 'function') window.showLoginModal();
      return;
    }
  }
"""
    switch_idx = t.find("function switchTab(tabId){")
    if switch_idx >= 0:
        brace_end = t.find("{", switch_idx) + 1
        t = t[:brace_end] + "\n" + guard + t[brace_end:]
        print("Login guard added")

# 4. Update cleanup for strategic panels
old_cleanup = "if(tabId!=='incendios'&&typeof limpiarIncendios==='function')limpiarIncendios();if(tabId!=='huracanes'&&typeof limpiarHuracanes==='function')limpiarHuracanes();"
new_cleanup = """if(tabId!=='incendios'&&typeof limpiarIncendios==='function')limpiarIncendios();if(tabId!=='huracanes'&&typeof limpiarHuracanes==='function')limpiarHuracanes();
  if(tabId!=='trenes'&&tabId!=='polos'&&tabId!=='subsidios'&&tabId!=='selvamaya'){['seccion-trenes','seccion-polos','seccion-subsidios','seccion-selvamaya'].forEach(function(id){var e=document.getElementById(id);if(e)e.classList.remove('visible');});}"""
if old_cleanup in t:
    t = t.replace(old_cleanup, new_cleanup, 1)
    print("Cleanup updated")

p.write_text(t, encoding="utf-8")
print(f"Final app.js: {len(t)}")
