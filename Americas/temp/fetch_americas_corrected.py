import urllib.request
import json
import ssl
import time
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

countries = {
    # Central America
    "belize.geojson": "BLZ",
    "costa_rica.geojson": "CRI",
    "el_salvador.geojson": "SLV",
    "guatemala.geojson": "GTM",
    "honduras.geojson": "HND",
    "nicaragua.geojson": "NIC",
    "panama.geojson": "PAN",
    
    # South America
    "bolivia.geojson": "BOL",
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

existing_files = os.listdir(out_dir)

for filename, code in countries.items():
    # Check if a variant of the file already exists to avoid repeating
    base_name = filename.split('.')[0]
    skip = False
    for ext in ['.json', '.geojson']:
        if f"{base_name}{ext}" in existing_files or f"mainland_{base_name}{ext}" in existing_files or f"{base_name}_mainland{ext}" in existing_files:
            skip = True
            break
            
    if skip:
        print(f"Skipping {filename}, already exists in some form.")
        continue

    url = f"https://raw.githubusercontent.com/johan/world.geo.json/master/countries/{code}.geo.json"
    out_path = f"{out_dir}\\{filename}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode())
            
            if data.get("type") == "Feature":
                data = {"type": "FeatureCollection", "features": [data]}
                
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(data, f)
            print(f"Saved {filename}")
    except Exception as e:
        print(f"Error fetching {filename}: {e}")
    time.sleep(0.5)
