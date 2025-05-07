import csv
import json
import os
from listscraper.instance_class import ScrapeInstance

TMDB_CATALOG_DIR = os.path.join("catalog", "movie")
os.makedirs(TMDB_CATALOG_DIR, exist_ok=True)

files = {
    "watchlist.csv": "watchlist.json",
    "favorites.csv": "favorites.json",
    "letterboxd_everyone_should_watch.csv": "letterboxd_everyone_should_watch.json"
}

for csv_file, json_file in files.items():
    metas = []
    with open(csv_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row['Name']
            year = row['Year']
            if not title:
                continue
            metas.append({
                "name": title,
                "type": "movie",
                "id": f"tmdb:{title.lower().replace(' ', '_')}_{year}",  # placeholder id
                "poster": "",  # you can enhance this using TMDB API later
                "description": ""
            })

    with open(os.path.join(TMDB_CATALOG_DIR, json_file), 'w', encoding='utf-8') as out:
        json.dump({"metas": metas}, out, indent=2, ensure_ascii=False)

    print(f"Converted {csv_file} → {json_file}")
