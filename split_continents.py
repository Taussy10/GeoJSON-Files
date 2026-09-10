import os
import requests
import json

base_path = r"E:\Tausif\animations\data"
url = 'https://raw.githubusercontent.com/GeoGuess/GeoGuess-Maps/main/public/geojson/areas/continents.geojson'

res = requests.get(url)
if res.status_code == 200:
    data = res.json()
    continents = {}
    
    for feature in data['features']:
        cont_name = feature['properties'].get('continent')
        if not cont_name: continue
        
        file_name = cont_name.lower().replace(" ", "_")
        if file_name not in continents:
            continents[file_name] = []
        continents[file_name].append(feature)
        
    for file_name, features in continents.items():
        geojson_data = {
            "type": "FeatureCollection",
            "features": features
        }
        file_path = os.path.join(base_path, f"{file_name}.json")
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(geojson_data, f)
        print(f"Saved {file_path}")
else:
    print("Failed to download continents data")
