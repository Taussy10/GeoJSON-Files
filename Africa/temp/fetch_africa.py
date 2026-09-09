import urllib.request
import json
import ssl
import time
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

countries = {
    "algeria.geojson": "DZA",
    "angola.geojson": "AGO",
    "benin.geojson": "BEN",
    "botswana.geojson": "BWA",
    "burkina_faso.geojson": "BFA",
    "burundi.geojson": "BDI",
    "cabo_verde.geojson": "CPV",
    "cameroon.geojson": "CMR",
    "central_african_republic.geojson": "CAF",
    "chad.geojson": "TCD",
    "comoros.geojson": "COM",
    "congo.geojson": "COG",
    "dr_congo.geojson": "COD",
    "djibouti.geojson": "DJI",
    "equatorial_guinea.geojson": "GNQ",
    "eritrea.geojson": "ERI",
    "eswatini.geojson": "SWZ",
    "ethiopia.geojson": "ETH",
    "gabon.geojson": "GAB",
    "gambia.geojson": "GMB",
    "ghana.geojson": "GHA",
    "guinea.geojson": "GIN",
    "guinea_bissau.geojson": "GNB",
    "ivory_coast.geojson": "CIV",
    "kenya.geojson": "KEN",
    "lesotho.geojson": "LSO",
    "liberia.geojson": "LBR",
    "libya.geojson": "LBY",
    "madagascar.geojson": "MDG",
    "malawi.geojson": "MWI",
    "mali.geojson": "MLI",
    "mauritania.geojson": "MRT",
    "mauritius.geojson": "MUS",
    "mozambique.geojson": "MOZ",
    "namibia.geojson": "NAM",
    "niger.geojson": "NER",
    "rwanda.geojson": "RWA",
    "sao_tome_and_principe.geojson": "STP",
    "senegal.geojson": "SEN",
    "seychelles.geojson": "SYC",
    "sierra_leone.geojson": "SLE",
    "somalia.geojson": "SOM",
    "south_sudan.geojson": "SSD",
    "sudan.geojson": "SDN",
    "tanzania.geojson": "TZA",
    "togo.geojson": "TGO",
    "tunisia.geojson": "TUN",
    "uganda.geojson": "UGA",
    "zambia.geojson": "ZMB",
    "zimbabwe.geojson": "ZWE"
}

out_dir = r"E:\Tausif\animations\data\Africa"
existing_files = os.listdir(out_dir)

for filename, code in countries.items():
    base_name = filename.split('.')[0]
    skip = False
    for ext in ['.json', '.geojson']:
        if f"{base_name}{ext}" in existing_files or f"mainland_{base_name}{ext}" in existing_files or f"{base_name}_mainland{ext}" in existing_files:
            skip = True
            break
            
    if skip:
        print(f"Skipping {filename}, already exists.")
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
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"File not found on Github for {filename} ({code}).")
        else:
            print(f"Error fetching {filename}: {e}")
    except Exception as e:
        print(f"Error fetching {filename}: {e}")
    time.sleep(0.5)
