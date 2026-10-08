import pathlib, re

REPOS = [
    r"D:\CONANP\GITHUB\geovisor_plus",
    r"D:\CONANP\GITHUB\geovisor_plus_login",
    r"D:\CONANP\GITHUB\copilot-worktrees\Geovisor_opencode\ulsarahp-shiny-engine",
    r"D:\CONANP\GITHUB\copilot-worktrees\Geovisor_opencode\ulsarahp-scaling-system",
]

for repo in REPOS:
    R = pathlib.Path(repo)
    print(f"\n=== {R.name} ===")

    # 1. config.js: eliminar línea export (rompe script clásico)
    cfg = R / "assets" / "js" / "config.js"
    t = cfg.read_text(encoding="utf-8")
    new_t, n = re.subn(r"^export\s\{[^}]*\};\s*$", "", t, flags=re.MULTILINE)
    if n:
        cfg.write_text(new_t, encoding="utf-8")
        print(f"  config.js: {n} export eliminado")
    else:
        print("  config.js: sin export (ok)")

    # 2. main.js: quitar import/exports, exponer en window
    mjs = R / "assets" / "js" / "main.js"
    t = mjs.read_text(encoding="utf-8")
    orig = t
    t = re.sub(r"^import\s+'\.\/config\.js';\s*$", "", t, flags=re.MULTILINE)
    t = re.sub(r"^export\s+default\s+\w+;\s*$", "", t, flags=re.MULTILINE)
    t = re.sub(r"^export\s\{[^}]*\};\s*$", "", t, flags=re.MULTILINE)
    if t != orig and "window.APP_INFO" not in t:
        t += "\nwindow.APP_INFO = APP_INFO;\nwindow.environmentReport = environmentReport;\n"
    mjs.write_text(t, encoding="utf-8")
    print(f"  main.js: import/export {'eliminados' if t != orig else 'ya ausentes'} ({len(t)} chars)")

    # 3. index.html: module -> classic
    idx = R / "index.html"
    t = idx.read_text(encoding="utf-8")
    new_t, n = re.subn(
        r'<script type="module" src="assets/js/main\.js([^"]*)"></script>',
        r'<script src="assets/js/main.js\1"></script>',
        t
    )
    if n:
        idx.write_text(new_t, encoding="utf-8")
        print(f"  index.html: {n} script module → clásico")
    else:
        print("  index.html: sin module (ok)")
