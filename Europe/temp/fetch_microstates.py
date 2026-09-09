import urllib.request
import json
import time

relations = {
    "andorra.geojson": 9407,
    "liechtenstein.geojson": 1155955,
    "monaco.geojson": 1124039,
    "san_marino.geojson": 54624,
    "vatican_city.geojson": 36989
}

out_dir = r"E:\Tausif\animations\data\Europe"

for filename, rel_id in relations.items():
    url = f"https://polygons.openstreetmap.fr/get_geojson.py?id={rel_id}&params=0"
    out_path = f"{out_dir}\\{filename}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            feature_collection = {
                "type": "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "properties": {"name": filename.replace('.geojson', '').replace('_', ' ').title()},
                    "geometry": data
                }]
            }
            
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(feature_collection, f)
            print(f"Saved {filename}")
        time.sleep(1)
    except Exception as e:
        print(f"Error fetching {filename}: {e}")
