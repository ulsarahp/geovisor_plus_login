import pathlib, re

W = pathlib.Path("D:/CONANP/GITHUB/geovisor_plus_login")
html = (W/"index.html").read_text(encoding="utf-8")

# Inline CSS
for css_name in ["app.css", "plus_sections.css", "login_sections.css"]:
    p = W/"assets"/"css"/css_name
    if p.exists():
        code = p.read_text(encoding="utf-8")
        html = re.sub(
            r'<link rel="stylesheet" href="assets/css/' + css_name + r'[^"]*" />',
            lambda m: "<style>\n" + code + "\n</style>",
            html
        )

# Inline JS
for js_name in ["anti_fouc.js", "login.js", "config.js", "incendios.js", "huracanes.js", "app.js", "features.js", "metadata.js", "disclaimer.js"]:
    p = W/"assets"/"js"/js_name
    if p.exists():
        code = p.read_text(encoding="utf-8")
        html = re.sub(
            r'<script src="assets/js/' + js_name + r'[^"]*"></script>',
            lambda m, c=code: "<script>\n" + c + "\n</script>",
            html
        )

# Main.js
main = (W/"assets"/"js"/"main.js").read_text(encoding="utf-8").replace("\r\n", "\n")
main_stripped = re.sub(r"^import\s.*?;\s*$", "", main, flags=re.MULTILINE | re.DOTALL)
main_stripped = re.sub(r"^export\s.*$", "", main_stripped, flags=re.MULTILINE).strip()
html = re.sub(
    r'<script type="module" src="assets/js/main\.js[^"]*"></script>',
    lambda m: "<script>\n" + main_stripped + "\n</script>",
    html
)

(W/"geovisor_plus_login_single.html").write_text(html, encoding="utf-8")
print(f"Single: {len(html)} chars, {len(html.splitlines())} lines")
