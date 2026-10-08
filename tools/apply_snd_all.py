import pathlib, re, shutil

REPOS = [
    r"D:\CONANP\GITHUB\geovisor_plus",
    r"D:\CONANP\GITHUB\geovisor_plus_login",
    r"D:\CONANP\GITHUB\copilot-worktrees\Geovisor_opencode\ulsarahp-shiny-engine",
    r"D:\CONANP\GITHUB\copilot-worktrees\Geovisor_opencode\ulsarahp-scaling-system",
]

# Fuente de verdad: snd_styles.css del repo login
SRC = pathlib.Path(r"D:\CONANP\GITHUB\geovisor_plus_login\assets\css\snd_styles.css")
SND = SRC.read_text(encoding="utf-8")

# 1. Fuentes oficiales SND (Montserrat + Noto Sans + Source Code Pro)
OLD_FONTS = re.compile(
    r'<link href="https://fonts\.googleapis\.com/css2\?[^"]*" rel="stylesheet" />'
)
NEW_FONTS = (
    '<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900'
    '&family=Noto+Sans:ital,wght@0,100..900;1,100..900&family=Source+Code+Pro:wght@200..900'
    '&display=swap" rel="stylesheet" />'
)

for repo in REPOS:
    R = pathlib.Path(repo)
    name = R.name
    print(f"\n=== {name} ===")

    # 2. Copiar snd_styles.css
    dst = R / "assets" / "css" / "snd_styles.css"
    dst.write_text(SND, encoding="utf-8")
    print(f"  snd_styles.css copiado ({len(SND)} chars)")

    # 3. Actualizar index.html: fuentes + link snd_styles al final del CSS
    idx = R / "index.html"
    t = idx.read_text(encoding="utf-8")

    # Fuentes
    t, nf = OLD_FONTS.subn(NEW_FONTS, t)
    print(f"  fonts.googleapis actualizado: {nf} vez/veces")

    # Link snd_styles después del último CSS propio (antes del primer <script> o después de app.css)
    if "snd_styles.css" not in t:
        link = '\n  <link rel="stylesheet" href="assets/css/snd_styles.css" />'
        # Insertar después del último link de css propio
        css_links = list(re.finditer(r'<link rel="stylesheet" href="assets/css/[^"]+" />', t))
        if css_links:
            last = css_links[-1]
            t = t[:last.end()] + link + t[last.end():]
            print("  link snd_styles.css insertado tras el último CSS")
        else:
            t = t.replace("</head>", f"  {link}\n</head>")
            print("  link snd_styles.css insertado antes de </head>")
    else:
        print("  link snd_styles.css ya presente")

    idx.write_text(t, encoding="utf-8")
    print(f"  index.html: {len(t)} chars")
