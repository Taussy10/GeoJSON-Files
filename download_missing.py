import os
import requests
import json
import time

missing = {
    "Americas": ["antigua_and_barbuda", "barbados", "dominica", "grenada", "saint_kitts_and_nevis", "saint_lucia", "saint_vincent_and_the_grenadines"],
    "Asia": ["bahrain", "maldives"],
    "Africa": ["cabo_verde", "comoros", "mauritius", "sao_tome_and_principe", "seychelles"],
    "Oceania": ["fiji", "kiribati", "marshall_islands", "micronesia", "nauru", "new_zealand", "palau", "papua_new_guinea", "solomon_islands", "tonga", "tuvalu", "vanuatu"]
}

base_path = r"E:\Tausif\animations\data"

for region, countries in missing.items():
    region_dir = os.path.join(base_path, region)
    os.makedirs(region_dir, exist_ok=True)
    for country in countries:
        file_path = os.path.join(region_dir, f"{country}.json")
        search_term = country.replace("_", " ")
        if country == "sao_tome_and_principe": search_term = "Sao Tome and Principe"
        
        url = f"https://nominatim.openstreetmap.org/search?country={search_term}&polygon_geojson=1&format=json&limit=1"
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
                                    "name": search_term.title()
                                },
                                "geometry": data[0]['geojson']
                            }
                        ]
                    }
                    with open(file_path, "w") as f:
                        json.dump(geojson_data, f)
                    print(f"Downloaded {country}")
                else:
                    print(f"No geojson found for {country}")
            else:
                print(f"Error fetching {country}: {res.status_code}")
        except Exception as e:
            print(f"Exception on {country}: {e}")
        time.sleep(1) # Be nice to the API
