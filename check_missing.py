import os

# Complete list of 195 sovereign states grouped by continent/region

regions = {
    "Europe": [
        "albania", "andorra", "austria", "belarus", "belgium", "bosnia_and_herzegovina",
        "bulgaria", "croatia", "cyprus", "czechia", "denmark", "estonia", "finland",
        "france", "germany", "greece", "hungary", "iceland", "ireland", "italy",
        "kosovo", "latvia", "liechtenstein", "lithuania", "luxembourg", "malta",
        "moldova", "monaco", "montenegro", "netherlands", "north_macedonia", "norway",
        "poland", "portugal", "romania", "russia", "san_marino", "serbia", "slovakia",
        "slovenia", "spain", "sweden", "switzerland", "ukraine", "united_kingdom", "vatican_city"
    ],
    "Americas": [
        "antigua_and_barbuda", "argentina", "bahamas", "barbados", "belize", "bolivia",
        "brazil", "canada", "chile", "colombia", "costa_rica", "cuba", "dominica",
        "dominican_republic", "ecuador", "el_salvador", "grenada", "guatemala", "guyana",
        "haiti", "honduras", "jamaica", "mexico", "nicaragua", "panama", "paraguay",
        "peru", "saint_kitts_and_nevis", "saint_lucia", "saint_vincent_and_the_grenadines",
        "suriname", "trinidad_and_tobago", "united_states", "uruguay", "venezuela", "usa"
    ],
    "Asia": [
        "afghanistan", "armenia", "azerbaijan", "bahrain", "bangladesh", "bhutan",
        "brunei", "cambodia", "china", "georgia", "india", "indonesia", "iran",
        "iraq", "israel", "japan", "jordan", "kazakhstan", "kuwait", "kyrgyzstan",
        "laos", "lebanon", "malaysia", "maldives", "mongolia", "myanmar", "nepal",
        "north_korea", "oman", "pakistan", "palestine", "philippines", "qatar",
        "saudi_arabia", "singapore", "south_korea", "sri_lanka", "syria", "taiwan",
        "tajikistan", "thailand", "timor_leste", "turkey", "turkmenistan", "uae",
        "uzbekistan", "vietnam", "yemen"
    ],
    "Africa": [
        "algeria", "angola", "benin", "botswana", "burkina_faso", "burundi", "cabo_verde",
        "cameroon", "central_african_republic", "chad", "comoros", "congo", "dr_congo",
        "djibouti", "egypt", "equatorial_guinea", "eritrea", "eswatini", "ethiopia",
        "gabon", "gambia", "ghana", "guinea", "guinea_bissau", "ivory_coast", "kenya",
        "lesotho", "liberia", "libya", "madagascar", "malawi", "mali", "mauritania",
        "mauritius", "morocco", "mozambique", "namibia", "niger", "nigeria", "rwanda",
        "sao_tome_and_principe", "senegal", "seychelles", "sierra_leone", "somalia",
        "south_africa", "south_sudan", "sudan", "tanzania", "togo", "tunisia", "uganda",
        "zambia", "zimbabwe"
    ],
    "Oceania": [
        "australia", "fiji", "kiribati", "marshall_islands", "micronesia", "nauru",
        "new_zealand", "palau", "papua_new_guinea", "samoa", "solomon_islands", "tonga",
        "tuvalu", "vanuatu"
    ]
}

base_path = r"E:\Tausif\animations\data"

for region, countries in regions.items():
    region_path = os.path.join(base_path, region)
    
    if not os.path.exists(region_path):
        print(f"\n--- {region} ---")
        print(f"Folder does not exist: {region_path}")
        print("Missing all countries in this region.")
        continue
        
    existing_files = [f.lower() for f in os.listdir(region_path)]
    missing = []
    
    for country in countries:
        # Check for various formats: country.json, country.geojson, mainland_country.json, etc.
        # Also handle spaces vs underscores
        c1 = country.replace(' ', '_')
        c2 = country.replace('_', ' ')
        c3 = country.replace('_', '-')
        
        found = False
        for ext in ['.json', '.geojson']:
            for name in [c1, c2, c3]:
                variants = [
                    f"{name}{ext}",
                    f"mainland_{name}{ext}",
                    f"{name}_mainland{ext}",
                    f"republic_of_{name}{ext}"
                ]
                if any(v in existing_files for v in variants):
                    found = True
                    break
            if found: break
            
        # Hardcoded specific fallbacks just in case
        if country == "united_states" and any("usa" in f for f in existing_files): found = True
        if country == "uae" and any("united_arab_emirates" in f for f in existing_files): found = True
        if country == "czechia" and any("czech_republic" in f for f in existing_files): found = True
            
        if not found:
            missing.append(country)
            
    print(f"\n--- {region} ---")
    if missing:
        for m in missing:
            print(f"Missing: {m}")
    else:
        print("All countries present!")
