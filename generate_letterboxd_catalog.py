#!/usr/bin/env python3
import requests, time, json, os

# ——— CONFIG ———
TMDB_API_KEY  = os.getenv('TMDB_API_KEY')
BASE_LIST_URL = 'https://letterboxd.com/couchpotato00/list/movies-everyone-should-watch-at-least-once'
FILMS_JSON    = BASE_LIST_URL + '/films.json'
OUTPUT_DIR    = os.path.join('catalog','movie')
OUTPUT_FILE   = os.path.join(OUTPUT_DIR,'letterboxd_everyone_should_watch.json')
HEADERS       = {
  'User-Agent':'Mozilla/5.0',
  'Accept':'application/json'
}
# ————————————

os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1) Fetch all pages of the JSON feed
films = []; page = 1
while True:
    resp = requests.get(FILMS_JSON, params={'page':page}, headers=HEADERS)
    data = resp.json()
    batch = data.get('films') or []
    if not batch: break
    films.extend(batch)
    page += 1
    time.sleep(0.5)

# 2) Lookup TMDB and build your Omni metas
metas = []
for f in films:
    title = f.get('name'); year = f.get('year')
    params = {'api_key':TMDB_API_KEY,'query':title}
    if year: params['year']=year
    r = requests.get('https://api.themoviedb.org/3/search/movie',
                     params=params, headers=HEADERS).json()
    if r.get('results'):
        t = r['results'][0]
        metas.append({
          'id':         f"tmdb:{t['id']}",
          'type':       'movie',
          'name':       t['title'],
          'poster':     f"https://image.tmdb.org/t/p/w500{t.get('poster_path')}" if t.get('poster_path') else "",
          'description':t.get('overview','')
        })
    time.sleep(0.25)

# 3) Write out the Omni catalog
with open(OUTPUT_FILE,'w',encoding='utf-8') as out:
    json.dump({'metas':metas}, out, indent=2, ensure_ascii=False)
print(f"✔️ Wrote {len(metas)} entries to {OUTPUT_FILE}")
