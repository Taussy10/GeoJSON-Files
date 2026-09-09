import urllib.request
import json
import ssl
import time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Mapping filename to ISO 3166-1 alpha-3 code
countries = {
    # North America
    "canada.geojson": "CAN",
    "mainland_united_states.geojson": "USA",
    "mexico.geojson": "MEX",
    
    # Central America
    "belize.geojson": "BLZ",
    "costa_rica.geojson": "CRI",
    "el_salvador.geojson": "SLV",
    "guatemala.geojson": "GTM",
    "honduras.geojson": "HND",
    "nicaragua.geojson": "NIC",
    "panama.geojson": "PAN",
    
    # South America
    "argentina.geojson": "ARG",
    "bolivia.geojson": "BOL",
    "brazil.geojson": "BRA",
    "chile.geojson": "CHL",
    "colombia.geojson": "COL",
    "ecuador.geojson": "ECU",
    "guyana.geojson": "GUY",
    "paraguay.geojson": "PRY",
    "peru.geojson": "PER",
    "suriname.geojson": "SUR",
    "uruguay.geojson": "URY",
    "venezuela.geojson": "VEN",
    
    # Caribbean
    "antigua_and_barbuda.geojson": "ATG",
    "bahamas.geojson": "BHS",
    "barbados.geojson": "BRB",
    "cuba.geojson": "CUB",
    "dominica.geojson": "DMA",
    "dominican_republic.geojson": "DOM",
    "grenada.geojson": "GRD",
    "haiti.geojson": "HTI",
    "jamaica.geojson": "JAM",
    "saint_kitts_and_nevis.geojson": "KNA",
    "saint_lucia.geojson": "LCA",
    "saint_vincent_and_the_grenadines.geojson": "VCT",
    "trinidad_and_tobago.geojson": "TTO"
}

out_dir = r"E:\Tausif\animations\data\Americas"

for filename, code in countries.items():
    url = f"https://raw.githubusercontent.com/johan/world.geo.json/master/countries/{code}.geo.json"
    out_path = f"{out_dir}\\{filename}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode())
            
            # Wrap in FeatureCollection if needed
            if data.get("type") == "Feature":
                data = {
                    "type": "FeatureCollection",
                    "features": [data]
                }
                
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(data, f)
            print(f"Saved {filename}")
    except urllib.error.HTTPError as e:
        print(f"Error fetching {filename} ({code}): HTTP {e.code}")
    except Exception as e:
        print(f"Error fetching {filename}: {e}")
    time.sleep(0.5)
