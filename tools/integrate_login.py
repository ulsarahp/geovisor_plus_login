import pathlib, re

W = pathlib.Path("D:/CONANP/GITHUB/geovisor_plus_login")
p = W/"index.html"
t = p.read_text(encoding="utf-8")
print(f"Original: {len(t)}")

# ================================================================
# 1. Añadir pestañas estratégicas (Trenes, Polos, Subsidios, Selva Maya)
# ================================================================
hur_pat = re.compile(r'<button[^>]*data-tab="huracanes"[^>]*>.*?</button>')
m = hur_pat.search(t)
if m:
    new_tabs = m.group(0) + """
          <button class="tab tab-estrategica" data-tab="trenes" style="display:none;"><i class="fas fa-train"></i> Trenes</button>
          <button class="tab tab-estrategica" data-tab="polos" style="display:none;"><i class="fas fa-map-pin"></i> Polos</button>
          <button class="tab tab-estrategica" data-tab="subsidios" style="display:none;"><i class="fas fa-hand-holding-dollar"></i> Subsidios</button>
          <button class="tab tab-estrategica" data-tab="selvamaya" style="display:none;"><i class="fas fa-tree"></i> Selva Maya</button>"""
    t = t[:m.start()] + new_tabs + t[m.end():]
    print("1. Strategic tabs added")

# ================================================================
# 2. Añadir botón login en header (antes de las tabs)
# ================================================================
if 'btn-login-toggle' not in t:
    login_btn = '<button id="btn-login-toggle" class="btn-login-toggle" title="Acceso estratégico" aria-label="Acceso estratégico"><i class="fas fa-lock"></i></button>'
    # Insertar antes del nav de tabs
    t = t.replace('<nav class="header-tabs">', login_btn + '\n          <nav class="header-tabs">', 1)
    print("2. Login button added")

# ================================================================
# 3. Añadir CSS login + secciones estratégicas
# ================================================================
if 'login_sections.css' not in t:
    t = t.replace('<link rel="stylesheet" href="assets/css/plus_sections.css"',
                  '<link rel="stylesheet" href="assets/css/login_sections.css" />\n  <link rel="stylesheet" href="assets/css/plus_sections.css"', 1)
    print("3. Login CSS added")

# ================================================================
# 4. Añadir script login.js (antes de config.js)
# ================================================================
if 'login.js' not in t:
    t = t.replace('<script src="assets/js/config.js',
                  '<script src="assets/js/login.js"></script>\n  <script src="assets/js/config.js', 1)
    print("4. Login script added")

# ================================================================
# 5. Añadir paneles para secciones estratégicas (en sidebar)
# ================================================================
if 'seccion-trenes' not in t:
    estrategicas_panels = """
    <!-- TRENES PANEL -->
    <div class="seccion-panel-estrategica" id="seccion-trenes">
      <div class="seccion-titulo"><i class="fas fa-train" style="color:#6F4489;"></i> Trenes</div>
      <div class="estrategica-placeholder">
        <i class="fas fa-train"></i>
        <div class="estrategica-title">Módulo Trenes</div>
        <p>Visualización de corredores ferroviarios y su intersección con ANP.<br>Contenido en construcción.</p>
      </div>
    </div>

    <!-- POLOS DEL BIENESTAR PANEL -->
    <div class="seccion-panel-estrategica" id="seccion-polos">
      <div class="seccion-titulo"><i class="fas fa-map-pin" style="color:#6F4489;"></i> Polos del Bienestar</div>
      <div class="estrategica-placeholder">
        <i class="fas fa-map-pin"></i>
        <div class="estrategica-title">Polos del Bienestar</div>
        <p>Ubicación de polos de desarrollo y su relación con áreas naturales protegidas.<br>Contenido en construcción.</p>
      </div>
    </div>

    <!-- SUBSIDIOS PANEL -->
    <div class="seccion-panel-estrategica" id="seccion-subsidios">
      <div class="seccion-titulo"><i class="fas fa-hand-holding-dollar" style="color:#6F4489;"></i> Programas de Subsidio</div>
      <div class="estrategica-placeholder">
        <i class="fas fa-hand-holding-dollar"></i>
        <div class="estrategica-title">Programas de Subsidio</div>
        <p>Distribución de subsidios por ANP y región.<br>Contenido en construcción.</p>
      </div>
    </div>

    <!-- SELVA MAYA PANEL -->
    <div class="seccion-panel-estrategica" id="seccion-selvamaya">
      <div class="seccion-titulo"><i class="fas fa-tree" style="color:#6F4489;"></i> Selva Maya</div>
      <div class="estrategica-placeholder">
        <i class="fas fa-tree"></i>
        <div class="estrategica-title">Selva Maya</div>
        <p>Monitoreo de la Selva Maya: ANP, deforestación, conectividad.<br>Contenido en construcción.</p>
      </div>
    </div>

    <!-- SUBTEMAS DASHBOARD (estratégico) -->
    <div id="dashboard-subtemas" style="display:none;">
      <span class="subtema-label"><i class="fas fa-chart-line"></i> Dashboard Estratégico:</span>
      <button data-subtema="trenes" onclick="switchSubtema('trenes')"><i class="fas fa-train"></i> Trenes</button>
      <button data-subtema="polos" onclick="switchSubtema('polos')"><i class="fas fa-map-pin"></i> Polos</button>
      <button data-subtema="subsidios" onclick="switchSubtema('subsidios')"><i class="fas fa-hand-holding-dollar"></i> Subsidios</button>
      <button data-subtema="selvamaya" onclick="switchSubtema('selvamaya')"><i class="fas fa-tree"></i> Selva Maya</button>
    </div>

    """
    # Insertar después del panel de huracanes
    hur_panel_end = t.find('</div>\n\n    <div id="grafico-anp-conteo"')
    if hur_panel_end >= 0:
        t = t[:hur_panel_end+7] + "\n" + estrategicas_panels + t[hur_panel_end+7:]
        print("5. Strategic panels added")
    else:
        # Fallback: insertar antes de grafico-anp-conteo
        grafico_idx = t.find('<div id="grafico-anp-conteo"')
        if grafico_idx >= 0:
            t = t[:grafico_idx] + estrategicas_panels + t[grafico_idx:]
            print("5. Strategic panels added (before grafico)")

# ================================================================
# 6. Actualizar título
# ================================================================
t = t.replace("Geovisor Plus CONANP", "Geovisor Plus Login CONANP")
t = t.replace("Geovisor Plus", "Geovisor Plus Login")

p.write_text(t, encoding="utf-8")
print(f"Final: {len(t)}")
