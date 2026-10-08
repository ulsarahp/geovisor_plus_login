import pathlib, re
from collections import Counter

W = pathlib.Path("D:/CONANP/GITHUB/geovisor_plus_login")
t = (W/"assets"/"css"/"app.css").read_text(encoding="utf-8")
print(f"app.css: {len(t)} chars")
colors = re.findall(r"#[0-9a-fA-F]{6}\b", t)
print("Colores más usados:", Counter(colors).most_common(15))
fonts = set(re.findall(r"font-family:\s*([^;]+);", t))
print("Familias:", fonts)

html = (W/"index.html").read_text(encoding="utf-8")
for m in re.finditer(r'<link[^>]*fonts\.googleapis[^>]*>', html):
    print(m.group(0))
