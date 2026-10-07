import pathlib, re

W = pathlib.Path("D:/CONANP/GITHUB/geovisor_plus_login")
p = W/"assets"/"js"/"app.js"
t = p.read_text(encoding="utf-8")

# Fix: encontrar el BLOQUE COMPLETO del huracanes else-if (incluyendo el cierre })
# y insertar los nuevos else-if DESPUÉS del cierre

# Buscar el final del bloque huracanes: "gAdvc.style.display='none';" seguido de "}"
hur_pat = re.compile(r"(else if\(tabId==='huracanes'\)\{.*?gAdvc\.style\.display='none';\s*\})", re.DOTALL)
m = hur_pat.search(t)

if m:
    huracanes_block = m.group(1)
    new_blocks = huracanes_block + """
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

    t = t[:m.start(1)] + new_blocks + t[m.end(1):]
    p.write_text(t, encoding="utf-8")
    print("Strategic sections properly added AFTER huracanes closing brace")
    print(f"app.js: {len(t)}")
else:
    print("Could not find huracanes block end pattern")
    # Show what's there to debug
    i = t.find("tabId==='huracanes'")
    seg = t[i:i+500]
    print(repr(seg[:300]))
