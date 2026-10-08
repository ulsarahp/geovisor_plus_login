import pathlib, re

R = pathlib.Path("D:/CONANP/GITHUB/geovisor_plus_login")
idx = (R/"index.html").read_text(encoding="utf-8")
# Líneas con app.css y anti_fouc.js
for pat in [r'.*app\.css.*', r'.*anti_fouc.*', r'.*snd_styles.*', r'.*config\.js.*']:
    for m in re.finditer(pat, idx):
        print(repr(m.group(0)[:160]))
    print("---")
