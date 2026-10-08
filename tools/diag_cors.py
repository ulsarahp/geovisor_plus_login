import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print("=== 1. GeoServer con Origin (reproducir CORS) ===")
url = "https://geoserver.conanp.gob.mx/geoserver/SIG-DES/wfs?service=WFS&version=1.1.0&request=GetFeature&typeName=SIG-DES:shp_anp&outputFormat=application/json&maxFeatures=1"
req = urllib.request.Request(url, headers={
    "Origin": "https://sig.conanp.gob.mx",
    "User-Agent": "Mozilla/5.0"
})
try:
    with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
        print("Status:", r.status)
        ac = r.headers.get_all("Access-Control-Allow-Origin")
        print("ACAO headers:", ac)
        print("Otros CORS:", {k: v for k, v in r.headers.items() if "Access-Control" in k})
except Exception as e:
    print("Error:", e)

print("\n=== 2. Local data deployada en produccion? ===")
for path in [
    "https://sig.conanp.gob.mx/visor_sig_des/assets/data/shp_anp.geojson",
    "https://sig.conanp.gob.mx/visor_sig_des/assets/js/config.js",
    "https://sig.conanp.gob.mx/visor_sig_des/assets/data/shp_advc.geojson",
]:
    try:
        req = urllib.request.Request(path, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
            print(f"  {r.status} {path}")
    except Exception as e:
        print(f"  FALLO {path} -> {e}")
