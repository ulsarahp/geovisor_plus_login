// ================================================================
// LOGIN — Autenticación de usuarios
// Público: General, ADVC, Dashboard (sin sub-temas estratégicos)
// Estratégico (requiere login): Incendios, Huracanes, Trenes,
//   Polos del Bienestar, Programas de Subsidio, Selva Maya
// Dashboard sub-temas (requiere login): Trenes, Polos, Subsidios, Selva Maya
// ================================================================

const AUTH_USER = 'ulises.sandoval@conanp.gob.mx';
const AUTH_PASS = 'Conanp2025';
const AUTH_KEY = 'geovisor_plus_auth';
const AUTH_SESSION_KEY = 'geovisor_plus_session';

// Secciones y su visibilidad
const SECCIONES_PUBLICAS = ['general', 'advc', 'dashboard'];
const SECCIONES_ESTRATEGICAS = ['incendios', 'huracanes', 'trenes', 'polos', 'subsidios', 'selvamaya'];
const SUBTEMAS_DASHBOARD = ['trenes', 'polos', 'subsidios', 'selvamaya'];

let isLoggedIn = false;

// ================================================================
// CHECK AUTH STATE
// ================================================================

function checkAuth() {
  try {
    // Verificar sessionStorage (sesión activa en esta pestaña)
    if (sessionStorage.getItem(AUTH_SESSION_KEY) === 'true') {
      isLoggedIn = true;
      return true;
    }
    // Verificar localStorage (recordar)
    if (localStorage.getItem(AUTH_KEY) === 'true') {
      isLoggedIn = true;
      sessionStorage.setItem(AUTH_SESSION_KEY, 'true');
      return true;
    }
  } catch (e) {}
  isLoggedIn = false;
  return false;
}

// ================================================================
// LOGIN / LOGOUT
// ================================================================

function doLogin(email, password, remember) {
  email = (email || '').trim().toLowerCase();
  password = password || '';

  if (!email || !password) {
    return { ok: false, msg: 'Ingresa usuario y contraseña.' };
  }
  if (email !== AUTH_USER.toLowerCase() || password !== AUTH_PASS) {
    return { ok: false, msg: 'Usuario o contraseña incorrectos.' };
  }

  isLoggedIn = true;
  try {
    sessionStorage.setItem(AUTH_SESSION_KEY, 'true');
    if (remember) localStorage.setItem(AUTH_KEY, 'true');
  } catch (e) {}
  return { ok: true };
}

function doLogout() {
  isLoggedIn = false;
  try {
    sessionStorage.removeItem(AUTH_SESSION_KEY);
    localStorage.removeItem(AUTH_KEY);
  } catch (e) {}
  hideStrategicSections();
  // Volver a General
  var generalTab = document.querySelector('.tab[data-tab="general"]');
  if (generalTab) generalTab.click();
}

// ================================================================
// UI: MODAL LOGIN
// ================================================================

function showLoginModal() {
  // Si ya existe, mostrar
  var existing = document.getElementById('login-modal');
  if (existing) { existing.style.display = 'flex'; return; }

  var modal = document.createElement('div');
  modal.id = 'login-modal';
  modal.style.cssText = 'display:none;position:fixed;inset:0;background:rgba(0,0,0,0.65);backdrop-filter:blur(6px);z-index:20000;align-items:center;justify-content:center;font-family:Inter,sans-serif;';
  modal.innerHTML = `
    <div style="background:var(--bg-surface,#fff);border:1px solid var(--border-medium,#ddd);border-radius:16px;width:100%;max-width:400px;padding:2rem;box-shadow:0 24px 64px rgba(0,0,0,0.4);">
      <div style="text-align:center;margin-bottom:1.4rem;">
        <div style="width:56px;height:56px;background:linear-gradient(135deg,#6B1132,#1a5c4e);border-radius:50%;margin:0 auto 0.8rem;display:flex;align-items:center;justify-content:center;">
          <i class="fas fa-lock" style="color:#fff;font-size:1.3rem;"></i>
        </div>
        <h2 style="font-family:'Space Grotesk',sans-serif;font-size:1.2rem;font-weight:800;color:var(--text-primary,#333);margin:0;">Acceso Estratégico</h2>
        <p style="font-size:0.72rem;color:var(--text-muted,#888);margin:0.4rem 0 0;">Ingresa para ver secciones estratégicas:<br>Trenes, Polos del Bienestar, Subsidios, Selva Maya</p>
      </div>
      <div style="display:flex;flex-direction:column;gap:0.8rem;">
        <div>
          <label style="font-size:0.65rem;font-weight:700;color:var(--text-muted,#888);text-transform:uppercase;letter-spacing:0.5px;display:block;margin-bottom:0.3rem;">Correo</label>
          <input type="email" id="login-email" placeholder="usuario@conanp.gob.mx"
            style="width:100%;padding:0.65rem 1rem;border:2px solid var(--border-medium,#ddd);border-radius:10px;font-size:0.85rem;font-family:Inter;background:var(--bg-glass,#f8f9fa);color:var(--text-primary,#333);outline:none;transition:border-color 0.2s;"
            onfocus="this.style.borderColor='#1a5c4e'" onblur="this.style.borderColor='var(--border-medium,#ddd)'">
        </div>
        <div>
          <label style="font-size:0.65rem;font-weight:700;color:var(--text-muted,#888);text-transform:uppercase;letter-spacing:0.5px;display:block;margin-bottom:0.3rem;">Contraseña</label>
          <input type="password" id="login-password" placeholder="••••••••"
            style="width:100%;padding:0.65rem 1rem;border:2px solid var(--border-medium,#ddd);border-radius:10px;font-size:0.85rem;font-family:Inter;background:var(--bg-glass,#f8f9fa);color:var(--text-primary,#333);outline:none;transition:border-color 0.2s;"
            onfocus="this.style.borderColor='#1a5c4e'" onblur="this.style.borderColor='var(--border-medium,#ddd)'"
            onkeydown="if(event.key==='Enter')window.tryLogin()">
        </div>
        <label style="display:flex;align-items:center;gap:0.5rem;font-size:0.72rem;color:var(--text-muted,#888);cursor:pointer;">
          <input type="checkbox" id="login-remember" style="width:16px;height:16px;accent-color:#1a5c4e;"> Recordarme en este equipo
        </label>
        <div id="login-error" style="display:none;font-size:0.72rem;color:#dc2626;background:#fef2f2;border:1px solid #fecaca;border-radius:8px;padding:0.5rem 0.8rem;"></div>
        <button id="login-submit" onclick="tryLogin()"
          style="width:100%;padding:0.7rem;background:linear-gradient(135deg,#6B1132,#8a1a3a);color:#fff;border:none;border-radius:10px;font-size:0.85rem;font-weight:700;cursor:pointer;font-family:Inter;transition:transform 0.15s;box-shadow:0 4px 12px rgba(107,17,50,0.3);">
          <i class="fas fa-sign-in-alt"></i> Ingresar
        </button>
        <button onclick="closeLoginModal()" style="width:100%;padding:0.5rem;background:transparent;color:var(--text-muted,#888);border:1px solid var(--border-subtle,#ddd);border-radius:10px;font-size:0.75rem;cursor:pointer;font-family:Inter;">Cancelar</button>
      </div>
      <div style="margin-top:1rem;text-align:center;font-size:0.6rem;color:var(--text-muted,#999);">
        <i class="fas fa-shield-alt"></i> Acceso restringido a personal autorizado CONANP
      </div>
    </div>
  `;
  document.body.appendChild(modal);
  modal.style.display = 'flex';
  // Focus en email
  setTimeout(function() { try { document.getElementById('login-email').focus(); } catch(e) {} }, 100);
}

function closeLoginModal() {
  var m = document.getElementById('login-modal');
  if (m) m.style.display = 'none';
}

function tryLogin() {
  var email = document.getElementById('login-email').value;
  var pass = document.getElementById('login-password').value;
  var remember = document.getElementById('login-remember').checked;
  var err = document.getElementById('login-error');

  var result = doLogin(email, pass, remember);
  if (result.ok) {
    closeLoginModal();
    showStrategicSections();
    // Si estábamos en una pestaña estratégica, recargar
    var currentTab = document.querySelector('.tab.active');
    if (currentTab && SECCIONES_ESTRATEGICAS.includes(currentTab.dataset.tab)) {
      currentTab.click();
    }
  } else {
    if (err) { err.textContent = result.msg; err.style.display = 'block'; }
  }
}

// ================================================================
// VISIBILIDAD DE SECCIONES
// ================================================================

function showStrategicSections() {
  SECCIONES_ESTRATEGICAS.forEach(function(tab) {
    var el = document.querySelector('.tab[data-tab="' + tab + '"]');
    if (el) el.style.display = '';
  });
  // Mostrar sub-temas del dashboard
  var subtemas = document.getElementById('dashboard-subtemas');
  if (subtemas) subtemas.style.display = 'flex';
  // Cambiar botón login → logout
  var btn = document.getElementById('btn-login-toggle');
  if (btn) {
    btn.innerHTML = '<i class="fas fa-sign-out-alt"></i>';
    btn.title = 'Cerrar sesión';
  }
  console.log('[Login] Secciones estratégicas visibles');
}

function hideStrategicSections() {
  SECCIONES_ESTRATEGICAS.forEach(function(tab) {
    var el = document.querySelector('.tab[data-tab="' + tab + '"]');
    if (el) el.style.display = 'none';
  });
  var subtemas = document.getElementById('dashboard-subtemas');
  if (subtemas) subtemas.style.display = 'none';
  var btn = document.getElementById('btn-login-toggle');
  if (btn) {
    btn.innerHTML = '<i class="fas fa-lock"></i>';
    btn.title = 'Acceso estratégico';
  }
  console.log('[Login] Secciones estratégicas ocultas');
}

// ================================================================
// INIT
// ================================================================

function initLogin() {
  console.log('[Login] Init');
  if (checkAuth()) {
    showStrategicSections();
  } else {
    hideStrategicSections();
  }
}

// Botón login/logout en el header
document.addEventListener('click', function(e) {
  var btn = e.target && e.target.closest ? e.target.closest('#btn-login-toggle') : null;
  if (!btn) return;
  e.preventDefault();
  e.stopPropagation();
  if (isLoggedIn) {
    doLogout();
  } else {
    showLoginModal();
  }
});

// Cerrar modal con Escape
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    var m = document.getElementById('login-modal');
    if (m && m.style.display === 'flex') closeLoginModal();
  }
});

// Cerrar modal clicando fuera
document.addEventListener('click', function(e) {
  var m = document.getElementById('login-modal');
  if (m && m.style.display === 'flex' && e.target === m) closeLoginModal();
});

// Init al cargar
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initLogin);
} else {
  initLogin();
}

window.doLogin = doLogin;
window.doLogout = doLogout;
window.tryLogin = tryLogin;
window.closeLoginModal = closeLoginModal;
window.showLoginModal = showLoginModal;
window.isLoggedIn = function() { return isLoggedIn; };
