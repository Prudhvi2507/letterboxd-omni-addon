#!/usr/bin/env python3
import pandas as pd, requests, json, os, time

# ——— CONFIG ———
TMDB_API_KEY  = '9eb9d41e0b5b419826bf6f7aed1a3d37'
CSV_FILE      = 'watchlist.csv'  # Export your Excel as CSV first
OUTPUT_DIR    = os.path.join('catalog', 'movie')
OUTPUT_FILE   = os.path.join(OUTPUT_DIR, 'recommended_drama_v2.json')
HEADERS       = {'User-Agent': 'Mozilla/5.0'}
# ————————————

os.makedirs(OUTPUT_DIR, exist_ok=True)

def tmdb_search(title, year):
    params = {'api_key': TMDB_API_KEY, 'query': title}
    if year:
        params['year'] = year
    r = requests.get(
        'https://api.themoviedb.org/3/search/movie',
        params=params, headers=HEADERS
    ).json()
    if r.get('results'):
        t = r['results'][0]
        return {
            'id':         f"tmdb:{t['id']}",
            'type':       'movie',
            'name':       t['title'],
            'poster':     (
                f"https://image.tmdb.org/t/p/w500{t['poster_path']}"
                if t.get('poster_path') else ""
            ),
            'description': t.get('overview', '')
        }
    return None

def main():
    df = pd.read_csv(CSV_FILE)
    metas = []

    for idx, row in df.iterrows():
        title = str(row.get('Name')).strip()
        year = str(row.get('Year')).strip()
        if not title or title.lower() == 'nan':
            continue
        print(f"[{idx+1}] {title} ({year}) → ", end='')
        m = tmdb_search(title, year)
        if m:
            metas.append(m)
            print("OK")
        else:
            print("FAIL")
        time.sleep(0.25)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        json.dump({'metas': metas}, out, indent=2, ensure_ascii=False)
    print(f"\nWrote {len(metas)} entries to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
