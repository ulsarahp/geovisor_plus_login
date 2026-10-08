import pathlib, re

R = pathlib.Path("D:/CONANP/GITHUB/geovisor_plus_login")
t = (R/"geovisor_plus_login_single.html").read_text(encoding="utf-8")
ext = re.findall(r'<script[^>]*src="([^"]+)"', t)
print("Scripts externos restantes:", ext)
links = re.findall(r'<link[^>]*href="([^"]+)"', t)
print("Links restantes:", [l for l in links if "assets" in l])
idx = (R/"index.html").read_text(encoding="utf-8")
tags = re.findall(r'<script[^>]*>', idx)
print("En index.html:")
for tag in tags:
    print("  ", tag)
