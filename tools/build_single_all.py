import pathlib, re

# Construye el single de un repo: inlinea TODOS los css/js en orden
REPO_SINGLE = {
    r"D:\CONANP\GITHUB\geovisor_plus": "geovisor_plus_single.html",
    r"D:\CONANP\GITHUB\geovisor_plus_login": "geovisor_plus_login_single.html",
    r"D:\CONANP\GITHUB\copilot-worktrees\Geovisor_opencode\ulsarahp-shiny-engine": "GeoTlacuilo_single.html",
    r"D:\CONANP\GITHUB\copilot-worktrees\Geovisor_opencode\ulsarahp-scaling-system": "GeoTlacuilo_single.html",
}

for repo, single_name in REPO_SINGLE.items():
    R = pathlib.Path(repo)
    html = (R / "index.html").read_text(encoding="utf-8")

    # Inline todos los CSS propios en orden (quitando query strings ?v=)
    def css_repl(m):
        p = R / m.group(1).split("?")[0]
        if p.exists():
            return "<style>\n" + p.read_text(encoding="utf-8") + "\n</style>"
        return m.group(0)

    html = re.sub(r'<link rel="stylesheet" href="(assets/css/[^"]+)" />', css_repl, html)

    # Inline todos los JS propios en orden (no-module)
    def js_repl(m):
        p = R / m.group(1).split("?")[0]
        if p.exists():
            return "<script>\n" + p.read_text(encoding="utf-8") + "\n</script>"
        return m.group(0)

    html = re.sub(r'<script src="(assets/js/[^"]+)"></script>', js_repl, html)

    # main.js (module) — quitar imports/exports
    def main_repl(m):
        p = R / m.group(1).split("?")[0]
        if p.exists():
            code = p.read_text(encoding="utf-8").replace("\r\n", "\n")
            code = re.sub(r"^import\s.*?;\s*$", "", code, flags=re.MULTILINE | re.DOTALL)
            code = re.sub(r"^export\s.*$", "", code, flags=re.MULTILINE).strip()
            return "<script>\n" + code + "\n</script>"
        return m.group(0)

    html = re.sub(r'<script type="module" src="(assets/js/main\.js[^"]*)"></script>', main_repl, html)

    out = R / single_name
    out.write_text(html, encoding="utf-8")
    snd_ok = "snd_styles" in html or "--pguinda900" in html
    print(f"{R.name}/{single_name}: {len(html)//1024}KB, SND inline: {snd_ok}")
