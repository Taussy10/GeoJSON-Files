import urllib.request
import json
import time

relations = {
    "albania.geojson": 53292,
    "bosnia_and_herzegovina.geojson": 2528142,
    "bulgaria.geojson": 186054,
    "croatia.geojson": 214885,
    "montenegro.geojson": 53296,
    "north_macedonia.geojson": 53293,
    "romania.geojson": 90689,
    "slovenia.geojson": 218657,
    "greenland.geojson": 214886
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
        time.sleep(1) # Be nice to the API
    except Exception as e:
        print(f"Error fetching {filename}: {e}")
