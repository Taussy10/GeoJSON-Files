import urllib.request
import json
import time

# Dictionary of country files to create and their corresponding OSM relation IDs
# Using specific OSM relations allows us to get just the mainland/contiguous parts
relations = {
    "sweden.geojson": 52822,
    "mainland_denmark.geojson": 50046,     # Denmark without Greenland/Faroe
    "mainland_norway.geojson": 2978650,    # Norway without Svalbard/Jan Mayen/Bouvet
    "finland.geojson": 54224,
    "iceland.geojson": 298022,
    "estonia.geojson": 79510,
    "latvia.geojson": 72594,
    "lithuania.geojson": 72596
}

out_dir = r"E:\Tausif\animations\data\Europe"

for filename, rel_id in relations.items():
    url = f"https://polygons.openstreetmap.fr/get_geojson.py?id={rel_id}&params=0"
    out_path = f"{out_dir}\\{filename}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            # Format as FeatureCollection
            feature_collection = {
                "type": "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "properties": {"name": filename.replace('.geojson', '').replace('mainland_', '').capitalize()},
                    "geometry": data
                }]
            }
            
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(feature_collection, f)
            print(f"Saved {filename}")
        time.sleep(1) # Be nice to the API
    except Exception as e:
        print(f"Error fetching {filename}: {e}")
