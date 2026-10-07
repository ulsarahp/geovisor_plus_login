import pathlib, urllib.request, json, os, sys

W = pathlib.Path("D:/CONANP/GITHUB/geovisor_plus_login/assets/data")
W.mkdir(parents=True, exist_ok=True)

# GeoServer base
BASE = "http://localhost:8081/geoserver/SIG-DES/wfs?"

# Capas a descargar
capas = [
    "shp_anp",
    "shp_advc",
    "shp_00ent",
    "shp_00mun",
    "shp_reg_conanp",
    "shp_reg_conanp_mex",
    "shp_zp_anp_mex",
    "shp_ramsar",
    "shp_ramsar_mex",
    "shp_kba_mex",
    "shp_unescomab_mex",
    "shp_unescopatrimonio_mex",
]

for capa in capas:
    url = f"{BASE}service=WFS&version=1.1.0&request=GetFeature&typeName=SIG-DES:{capa}&outputFormat=application/json"
    print(f"Descargando {capa}...", end=" ")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            # Verificar que es JSON válido
            j = json.loads(data)
            if j.get("type") != "FeatureCollection":
                print(f"ERROR: no es FeatureCollection")
                continue
            n = len(j.get("features", []))
            out = W / f"{capa}.geojson"
            out.write_bytes(data)
            print(f"OK ({n} features, {len(data)//1024}KB)")
    except Exception as e:
        print(f"FALLO: {e}")

# Listar archivos descargados
print("\n=== Archivos en assets/data ===")
for f in sorted(W.glob("*.geojson")):
    print(f"  {f.name}: {f.stat().st_size // 1024}KB")
