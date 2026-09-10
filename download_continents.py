import os
import requests
import json
import time

continents = {
    "asia": "Asia",
    "africa": "Africa",
    "europe": "Europe",
    "north_america": "North America",
    "south_america": "South America",
    "oceania": "Oceania",
    "australia": "Australia"
}

base_path = r"E:\Tausif\animations\data"

for filename, search_term in continents.items():
    file_path = os.path.join(base_path, f"{filename}.json")
    
    url = f"https://nominatim.openstreetmap.org/search?q={search_term.replace(' ', '+')}&polygon_geojson=1&format=json&limit=1"
    try:
        res = requests.get(url, headers={'User-Agent': 'TausifApp/1.0'})
        if res.status_code == 200:
            data = res.json()
            if len(data) > 0 and 'geojson' in data[0]:
                geojson_data = {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "properties": {
                                "name": search_term
                            },
                            "geometry": data[0]['geojson']
                        }
                    ]
                }
                with open(file_path, "w", encoding='utf-8') as f:
                    json.dump(geojson_data, f)
                print(f"Downloaded {filename}")
            else:
                print(f"No geojson found for {filename}")
        else:
            print(f"Error fetching {filename}: {res.status_code}")
    except Exception as e:
        print(f"Exception on {filename}: {e}")
    time.sleep(1.5)
