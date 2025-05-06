#!/usr/bin/env python3
import csv, requests, json, os, time

# ——— CONFIG ———
TMDB_API_KEY  = '9eb9d41e0b5b419826bf6f7aed1a3d37'
CSV_FILE      = 'recommended-drama.csv'
OUTPUT_DIR    = os.path.join('catalog','movie')
OUTPUT_FILE   = os.path.join(OUTPUT_DIR,'recommended-drama.json')
HEADERS       = {'User-Agent':'Mozilla/5.0'}
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
            'description': t.get('overview','')
        }
    return None

def main():
    # Read all lines, locate the header row that starts with "Position,"
    with open(CSV_FILE, encoding='utf-8') as f:
        lines = f.readlines()
    header_idx = next(i for i, line in enumerate(lines) if line.startswith('Position,'))
    data_lines = lines[header_idx:]  # from header onward

    reader = csv.DictReader(data_lines)
    metas = []
    for idx, row in enumerate(reader, 1):
        title = row['Name'].strip()
        year  = row['Year'].strip()
        if not title:
            continue
        print(f"[{idx}] {title} ({year}) → ", end='')
        m = tmdb_search(title, year)
        if m:
            metas.append(m)
            print("OK")
        else:
            print("FAIL")
        time.sleep(0.25)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        json.dump({'metas': metas}, out, indent=2, ensure_ascii=False)
    print(f"\nWrote {len(metas)} entries to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
