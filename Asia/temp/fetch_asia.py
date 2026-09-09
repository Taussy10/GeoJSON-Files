import urllib.request
import json
import ssl
import time
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

countries = {
    # Central Asia
    "kazakhstan.geojson": "KAZ",
    "kyrgyzstan.geojson": "KGZ",
    "tajikistan.geojson": "TJK",
    "turkmenistan.geojson": "TKM",
    "uzbekistan.geojson": "UZB",
    
    # South Asia
    "afghanistan.geojson": "AFG",
    "bhutan.geojson": "BTN",
    "maldives.geojson": "MDV",
    "nepal.geojson": "NPL",
    "pakistan.geojson": "PAK",
    "sri_lanka.geojson": "LKA",
    
    # Southeast Asia
    "brunei.geojson": "BRN",
    "cambodia.geojson": "KHM",
    "laos.geojson": "LAO",
    "malaysia.geojson": "MYS",
    "myanmar.geojson": "MMR",
    "philippines.geojson": "PHL",
    "thailand.geojson": "THA",
    "timor_leste.geojson": "TLS",
    "vietnam.geojson": "VNM",
    
    # East Asia
    "mongolia.geojson": "MNG",
    
    # West Asia
    "armenia.geojson": "ARM",
    "azerbaijan.geojson": "AZE",
    "bahrain.geojson": "BHR",
    "georgia.geojson": "GEO",
    "iraq.geojson": "IRQ",
    "jordan.geojson": "JOR",
    "kuwait.geojson": "KWT",
    "oman.geojson": "OMN",
    "qatar.geojson": "QAT",
    "syria.geojson": "SYR",
    "turkey.geojson": "TUR",
    "uae.geojson": "ARE"
}

out_dir = r"E:\Tausif\animations\data\Asia"

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
    except Exception as e:
        print(f"Error fetching {filename}: {e}")
    time.sleep(0.5)
