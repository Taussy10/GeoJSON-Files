import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries/GRL.geo.json"
try:
    with urllib.request.urlopen(url, context=ctx) as response:
        data = json.loads(response.read().decode())
        
    if data.get("type") == "Feature":
        data = {
            "type": "FeatureCollection",
            "features": [data]
        }
        
    with open(r"E:\Tausif\animations\data\Europe\greenland.geojson", "w", encoding="utf-8") as f:
        json.dump(data, f)
    print("Success: Downloaded greenland.geojson")
except Exception as e:
    print("Error:", e)
