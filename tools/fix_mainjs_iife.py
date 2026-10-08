import pathlib, re

REPOS = [
    r"D:\CONANP\GITHUB\geovisor_plus",
    r"D:\CONANP\GITHUB\geovisor_plus_login",
    r"D:\CONANP\GITHUB\copilot-worktrees\Geovisor_opencode\ulsarahp-shiny-engine",
    r"D:\CONANP\GITHUB\copilot-worktrees\Geovisor_opencode\ulsarahp-scaling-system",
]

for repo in REPOS:
    R = pathlib.Path(repo)
    p = R / "assets" / "js" / "main.js"
    t = p.read_text(encoding="utf-8")

    if t.lstrip().startswith("(function()"):
        print(f"{R.name}: ya es IIFE")
        continue

    # Envolver todo en IIFE para aislar las const del scope global
    # (colisionaban con los var de config.js al ser script clásico)
    body = t.rstrip() + "\n"
    new = "(function(){\n'use strict';\n" + body + "\n})();\n"
    p.write_text(new, encoding="utf-8")
    print(f"{R.name}: main.js envuelto en IIFE ({len(new)} chars)")
