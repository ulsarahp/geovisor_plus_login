import pathlib, re

REPOS = [
    r"D:\CONANP\GITHUB\geovisor_plus",
    r"D:\CONANP\GITHUB\geovisor_plus_login",
    r"D:\CONANP\GITHUB\copilot-worktrees\Geovisor_opencode\ulsarahp-shiny-engine",
    r"D:\CONANP\GITHUB\copilot-worktrees\Geovisor_opencode\ulsarahp-scaling-system",
]

# Mapeo a los valores oficiales SND (snd.gob.mx)
COLOR_MAP = {
    "#6B1132": "#611232",  # → pguinda900 (guinda oficial Gob.mx)
    "#6b1132": "#611232",
    "#8a1a3a": "#9B2247",  # → pguinda600
    "#8A1A3A": "#9B2247",
    "#4a0c22": "#4A0C26",  # → pguinda950
    "#4A0C22": "#4A0C26",
    "#1a5c4e": "#002F2A",  # → pverde900
    "#1A5C4E": "#002F2A",
    "#237660": "#004D40",  # → pverde600
    "#c0395a": "#A84565",  # → pguinda500
    "#6F4489": "#6708C1",  # → snd morado500
}

FONT_MAP = [
    ("'Inter', system-ui, sans-serif", "'Noto Sans', system-ui, sans-serif"),
    ("'Inter',sans-serif", "'Noto Sans',sans-serif"),
    ("'Inter', sans-serif", "'Noto Sans', sans-serif"),
    ("'Inter', sans-serif !important", "'Noto Sans', sans-serif !important"),
    ("'Inter',sans-serif !important", "'Noto Sans',sans-serif !important"),
    ("'Space Grotesk',sans-serif", "'Montserrat',sans-serif"),
    ("'Space Grotesk', sans-serif", "'Montserrat', sans-serif"),
    ("'Space Grotesk',monospace", "'Montserrat',monospace"),
    ('"Space Grotesk",sans-serif', "'Montserrat',sans-serif"),
]

for repo in REPOS:
    R = pathlib.Path(repo)
    print(f"\n=== {R.name} ===")
    total_c, total_f = 0, 0
    for css in (R / "assets" / "css").glob("*.css"):
        if css.name == "snd_styles.css":
            continue  # ya es oficial
        t = css.read_text(encoding="utf-8")
        orig = t
        nc, nf = 0, 0
        for old, new in COLOR_MAP.items():
            c = t.count(old)
            if c:
                t = t.replace(old, new)
                nc += c
        for old, new in FONT_MAP:
            c = t.count(old)
            if c:
                t = t.replace(old, new)
                nf += c
        if t != orig:
            css.write_text(t, encoding="utf-8")
            print(f"  {css.name}: {nc} colores, {nf} fuentes")
            total_c += nc
            total_f += nf
    print(f"  TOTAL: {total_c} colores → SND, {total_f} fuentes → SND")
