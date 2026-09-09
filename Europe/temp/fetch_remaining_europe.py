import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Dictionary of country files to create and their ISO 3166-1 alpha-3 codes
# We use github repo for these to avoid OSM server overload and guarantee quick downloads
countries = {
    "andorra.geojson": "AND",
    "austria.geojson": "AUT",
    "belarus.geojson": "BLR",
    "cyprus.geojson": "CYP",
    "czechia.geojson": "CZE",
    "hungary.geojson": "HUN",
    "ireland.geojson": "IRL",
    "liechtenstein.geojson": "LIE",
    "luxembourg.geojson": "LUX",
    "malta.geojson": "MLT",
    "moldova.geojson": "MDA",
    "monaco.geojson": "MCO",
    "poland.geojson": "POL",
    "san_marino.geojson": "SMR",
    "slovakia.geojson": "SVK",
    "switzerland.geojson": "CHE",
    "ukraine.geojson": "UKR",
    "vatican_city.geojson": "VAT"
}

out_dir = r"E:\Tausif\animations\data\Europe"

for filename, code in countries.items():
    url = f"https://raw.githubusercontent.com/johan/world.geo.json/master/countries/{code}.geo.json"
    out_path = f"{out_dir}\\{filename}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode())
            
            # Make sure it's wrapped in a FeatureCollection
            if data.get("type") == "Feature":
                data = {
                    "type": "FeatureCollection",
                    "features": [data]
                }
                
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
