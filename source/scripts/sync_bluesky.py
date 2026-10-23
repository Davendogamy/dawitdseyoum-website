#!/usr/bin/env python3
"""sync_bluesky.py — incremental self-update pipeline for dawitdseyoum.com

Fetches the artist's latest Bluesky posts (public API, no auth needed),
adds any NEW photo posts to the collection, and regenerates src/data/photos.ts.

Runs daily via GitHub Actions (.github/workflows/sync-bluesky.yml) and can be
run manually:  python scripts/sync_bluesky.py

Design guarantees:
- ADDITIVE: existing photographs (001-089) are never renamed, re-downloaded
  or dropped — their curation is frozen.
- STABLE IDs: new photos continue the numbering (090, 091, ...) regardless of
  how many arrive at once.
- SEEN-STATE: post rkeys + image CIDs recorded in scripts/sync_state.json,
  so nothing is imported twice.
- Parsing, curatorial overrides (MANUAL) and series classification are kept
  byte-identical to the original build_data.py so new work slots into
  The Witnesses / The Builders / The Commons exactly like the founding set.

Exit codes: 0 = ok (changes or not) · non-zero = hard failure (API down etc.)
"""
import json, os, re, subprocess, sys, unicodedata
from collections import Counter
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
IMG_DIR = os.path.join(ROOT, 'public', 'images')
CLEAN = os.path.join(SCRIPTS, 'photos_clean.json')
STATE = os.path.join(SCRIPTS, 'sync_state.json')
RAW = os.path.join(SCRIPTS, 'bsky_feed_raw.json')

ACTOR = 'dadasese69.bsky.social'
API = 'https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed'
MAX_PAGES = 5                      # 5 x 100 = up to 500 posts of history

os.makedirs(IMG_DIR, exist_ok=True)

# ---------------------------------------------------------------- fetch ----
def http_json(url):
    req = Request(url, headers={'User-Agent': 'dawitdseyoum-site-sync/1.0'})
    with urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))

def fetch_feed():
    params = {'actor': ACTOR, 'limit': 100, 'filter': 'posts_with_media'}
    items, cursor = [], None
    for _ in range(MAX_PAGES):
        if cursor:
            params['cursor'] = cursor
        data = http_json(API + '?' + urlencode(params))
        items.extend(data.get('feed', []))
        cursor = data.get('cursor')
        if not cursor:
            break
    return items

# ------------------------------------------------------------- parsing ----
def clean_text(t):
    return (t or '').replace('\u00a0', ' ').strip()

def slugify(s, maxlen=42):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode()
    s = re.sub(r"[^a-zA-Z0-9]+", '-', s).strip('-').lower()
    return s[:maxlen].rstrip('-') or 'untitled'

def parse_post(item, idx):
    post = item.get('post', {})
    if item.get('reason'):          # repost -> skip
        return None
    rec = post.get('record', {})
    text = clean_text(rec.get('text', ''))
    embed = post.get('embed', {})
    if embed.get('$type') != 'app.bsky.embed.images#view':
        return None                  # gallery needs images
    images = embed.get('images', [])
    if not images:
        return None
    if 'lensculture' in text.lower():
        return None                  # award announcements -> About page, not gallery
    img = images[0]
    full = img.get('fullsize', '')
    alt = clean_text(img.get('alt', ''))
    ar = img.get('aspectRatio') or {}
    rkey = post.get('uri', '').split('/')[-1]
    created = rec.get('createdAt', '')[:10]
    if not full:
        return None

    lines = [l.strip() for l in text.split('\n')]

    # title: quoted string on first line(s), or Title: X (anywhere)
    title = ''
    m = re.match(r'^(?:Photo[:\s]*)?["\u201c\u201d]([^"\u201c\u201d\n]+)["\u201c\u201d]', text)
    if m:
        title = m.group(1).strip()
    else:
        m = re.search(r'Title\s*[:=]\s*["\u201c]?\s*([^"\u201c\u201d\n]{3,80})', text, re.I)
        if m:
            title = m.group(1).strip().strip('"').strip()

    cid = full.rsplit('/', 1)[-1]

    fm = re.search(r'\bID[:=]\s*([A-Za-z0-9_.\-]+)', text)
    file_id = fm.group(1).strip().rstrip('.,') if fm else ''

    tm = re.search(r'\bTime[s]?:\s*([0-9]{1,2}:[0-9]{2}(?::[0-9]{2})?)', text)
    time_s = tm.group(1) if tm else ''

    tags = []
    for t in re.findall(r'#([A-Za-z0-9_]+)', text):
        if t.lower() not in [x.lower() for x in tags]:
            tags.append(t)

    # caption = text minus title line, ID/Time lines, hashtag lines
    keep = []
    for l in lines:
        if not l:
            keep.append('')
            continue
        if title and title.lower() in l.lower() and len(l) < len(title) + 14:
            continue
        if re.match(r'^(Photo[:\s]*)?["\u201c\u201d][^"\u201c\u201d]+["\u201c\u201d]\s*$', l):
            continue
        if re.match(r'^(ID|Id|id)[:=]', l) or re.match(r'^\s*Time[s]?\s*[:\s]', l) or re.match(r'^(Hours?|Captured|Date)[:]', l, re.I):
            continue
        if l.startswith('#'):
            continue
        if re.match(r'^@[A-Za-z0-9.\-]+$', l):   # pure @handle mention lines
            continue
        if re.match(r'^Photo by', l, re.I) or re.match(r'^@dadasese69', l, re.I):
            continue
        keep.append(l)
    cap = '\n'.join(keep)
    cap = re.sub(r'\n{3,}', '\n\n', cap).strip(' \n\t-').strip()
    if not title:
        first = [l for l in lines if l and not l.startswith('#') and not l.startswith('@')]
        title = (first[0][:48] if first else f'Untitled {idx}')
        title = title.strip('"')

    return {
        'rkey': rkey, 'title': title, 'caption': cap, 'alt': alt,
        'date': created, 'time': time_s, 'fileId': file_id, 'tags': tags,
        'full': full, 'cid': cid,
        'ar_w': int(ar.get('width', 0)), 'ar_h': int(ar.get('height', 0)),
        'bskyUrl': f"https://bsky.app/profile/dadasese69.bsky.social/post/{rkey}",
    }

# ------------------------------------------- curation (keep in sync!) -----
MANUAL = {
    ('2025-06-05', 'Sky Water'):            ('Sky Water', 'witnesses'),
    ('2025-06-17', 'A priceless lens'):     ('A Priceless Lens', 'commons'),
    ('2025-04-18', 'Real photograph'):      ('Architect and Archangel', 'builders'),
    ('2025-10-17', 'Three spies'):          ('Three Spies', 'commons'),
    ('2025-07-23', 'Photo'):                ('When the Signals Fade', 'witnesses'),
    ('2024-10-31', 'Time: 8:08:08'):        ('The Natural Tablecloth', 'commons'),
    ('2024-10-30', 'Date: 28/10/2024'):     ('The Long Winter', 'commons'),
    ('2024-10-24', '@dadasese69'):          ('Untitled (Urban Study)', 'commons'),
    ('2024-10-05', 'Untitled'):             ('Dog Walking', 'witnesses'),
    ('2025-01-09', 'Time: 13:33:30'):       ('Step, forward', 'witnesses'),
    ('2024-12-25', 'Christmas 2024'):       ("Duomo's Enduring Wings", 'builders'),
    ('2024-12-16', 'Italy, Time'):          ('Sunrise in Smog', 'commons'),
    ('2024-12-08', 'Italy, Milan'):         ('Wintery Morning', 'commons'),
    ('2025-04-16', '16 April 2025'):        ('The Sky People', 'commons'),
    ('2025-11-04', 'Man'):                  ("Man's Best Friend", 'witnesses'),
    ('2024-10-03', 'Urban Gaze'):           ('Urban Gaze', 'commons'),
    ('2026-09-30', 'Blue, green, red'):     ('Blue, green, red sanguine', 'commons'),
    ('2025-05-26', 'Plants mean flesh'):    ('Plants mean flesh?', 'commons'),
    ('2026-08-09', 'Sun, son song'):        ('Sun, son song sing sung', 'witnesses'),
    ('2025-05-11', 'Splash'):               ('Splash', 'witnesses'),
    ('2025-07-30', 'My beloved pet'):       ('My beloved pet', 'witnesses'),
    ('2025-03-03', 'A world without birds'):('A world without birds', 'witnesses'),
    # --- backfill editorial decisions (Oct 2026) ---
    ('2024-10-01', 'Captured at a quiet'):   ('Quiet, 6 a.m.', 'commons'),
    ('2024-08-10', "Nature's Palette"):      ("Nature's Palette: Ducks in a Blue-Hued River", 'witnesses'),
    ('2024-07-07', 'Skyline moments'):       ('Skyline moments', 'witnesses'),
    ('2024-04-27', 'One winter evening'):    ('One winter evening', 'commons'),
    ('2024-04-24', '@streetphotography'):    ('Street crossing, Milan', 'commons'),
    ('2024-04-19', 'I could not keep'):      ('Laika', 'witnesses'),
    ('2024-04-18', '@streetphotography'):    ('Morning walk, Bosco Verticale', 'builders'),
    ('2024-04-16', 'Nested within'):         ('A playground oasis', 'commons'),
    ('2024-04-14', 'Nestled within'):        ('Storied streets', 'commons'),
}
def apply_manual(p):
    for (d, pref), (t, s) in MANUAL.items():
        if p['date'] == d and p['title'].startswith(pref):
            p['title'], p['_series_override'] = t, s
            return

def tidy_title(t):
    t = re.sub(r'^(Time[s]?|Date|Hours?)\s*[:\s].*$', '', t).strip()
    return t or 'Untitled'

WIT = r'\b(heron|pigeon|crow|gull|seagull|swan|starling|duck|bird|cat|dog|sparrow|magpie|owl|wings?|feather|animal|oxen|snake|turtle|fish)\b'
BILD = r'\b(skyscraper|tower|scaffold|glass|facade|architecture|duomo|construction|building|buildings|contrail|skyline)\b'
OVERRIDES = {
    'curved dot': 'witnesses', 'fence to face': 'witnesses', 'bulb stars': 'witnesses',
    'hero with no job': 'witnesses', "i looked right": 'witnesses', 'my town, my city': 'witnesses',
    'majestic stones': 'builders', 'builders': 'builders', 'uno-credit': 'builders',
    'signed by the air': 'builders', 'a frame': 'builders', 'tide for the sky': 'builders',
    'architect and arcangel': 'builders',
    'three trees': 'commons', 'this is oxford': 'commons', 'the price of rain': 'commons',
    'noble gas': 'commons', 'shirtless': 'commons', 'urban gaze': 'commons',
    'martian': 'commons', 'the silent witness': 'commons', 'soft as delicate': 'commons',
    'the wachowskis': 'commons', 'three spies': 'commons', 'watchers': 'commons',
    'a soldier': 'commons', 'son': 'commons', 'the sky people': 'commons',
    'featherless': 'commons', 'adaptation and evolution': 'commons', 'a short tale': 'witnesses',
    'busy rush hours': 'commons', 'that is life': 'commons', 'first step': 'commons',
    'total recall': 'commons', 'we watch': 'commons', 'sit up': 'commons',
    'ominus bench': 'commons', 'neon light': 'commons', 'friction': 'commons',
    'a journey on planet': 'commons', 'invasion': 'commons', 'step by step': 'commons',
    'tree at no. 6': 'commons', 'twins in pair': 'commons', 'sunrise in smog': 'commons',
    # --- backfill series confirmations ---
    "nature's palette": 'witnesses', "nature\u2019s palette": 'witnesses',
    'skyline moments': 'witnesses', 'laika': 'witnesses',
    'bosco verticale': 'builders', 'playground oasis': 'commons',
    'storied streets': 'commons', 'one winter evening': 'commons',
}
def classify(p):
    hay = ' '.join([p['title'], p['caption'], p['alt']]).lower()
    for k, v in OVERRIDES.items():
        if k in hay:
            return v
    if re.search(WIT, hay, re.I):
        return 'witnesses'
    if re.search(BILD, hay, re.I):
        return 'builders'
    return 'commons'

# ----------------------------------------------------------- download ----
def dl(url, dest):
    for _ in range(3):
        try:
            r = subprocess.run(['curl', '-sL', '--max-time', '60', '-o', dest, url],
                               capture_output=True)
        except FileNotFoundError:                 # no curl -> stdlib fallback
            return dl_urllib(url, dest)
        if r.returncode == 0 and os.path.exists(dest) and os.path.getsize(dest) > 5000:
            return True
    return False

def dl_urllib(url, dest):
    try:
        req = Request(url, headers={'User-Agent': 'dawitdseyoum-site-sync/1.0'})
        with urlopen(req, timeout=60) as r, open(dest, 'wb') as f:
            f.write(r.read())
        return os.path.getsize(dest) > 5000
    except Exception:
        return False

def image_dims(dest, fallback):
    try:
        from PIL import Image
        with Image.open(dest) as im:
            w, h = im.size
        return w, h
    except Exception:
        pass
    w, h = fallback
    return (w, h) if (w and h) else (0, 0)

# --------------------------------------------------------------- main ----
def main():
    print(f"Fetching Bluesky feed of @{ACTOR} ...")
    try:
        feed = fetch_feed()
    except Exception as e:
        print(f"HARD FAILURE fetching feed: {e}")
        sys.exit(1)
    print(f"Fetched {len(feed)} feed items")
    with open(RAW, 'w') as f:
        json.dump({'fetchedAt': datetime.now(timezone.utc).isoformat(), 'feed': feed},
                  f, ensure_ascii=False, indent=1)

    # existing collection + seen-state
    photos = json.load(open(CLEAN)) if os.path.exists(CLEAN) else []
    state = {'seen_rkeys': [], 'seen_cids': []}
    if os.path.exists(STATE):
        state = json.load(open(STATE))
    if not state['seen_rkeys']:                     # bootstrap from existing data
        state['seen_rkeys'] = [p['bskyUrl'].rsplit('/', 1)[-1] for p in photos]
    known_rkeys = set(state['seen_rkeys'])
    known_cids = set(state['seen_cids'])

    # parse + dedupe the fresh feed
    parsed, seen_r, seen_c = [], set(), set()
    for item in feed:
        p = parse_post(item, len(parsed) + 1)
        if not p or p['rkey'] in seen_r:
            continue
        seen_r.add(p['rkey'])
        if p['cid'] in seen_c:
            continue
        seen_c.add(p['cid'])
        parsed.append(p)

    new = [p for p in parsed
           if p['rkey'] not in known_rkeys and p['cid'] not in known_cids]
    new.sort(key=lambda p: p['date'], reverse=True)   # newest first
    if not new:
        print("No new photographs — collection is up to date.")
        # refresh state file only if bootstrapped this run
        if not os.path.exists(STATE):
            json.dump(state, open(STATE, 'w'), indent=1)
        return

    # stable numbering: continue after the highest existing 001-xxx prefix
    max_num = 0
    for p in photos:
        m = re.match(r'^(\d{3})-', p['id'])
        if m:
            max_num = max(max_num, int(m.group(1)))
    print(f"New photographs to add: {len(new)} (continuing from {max_num:03d})")

    added = []
    for p in new:
        apply_manual(p)
        p['title'] = tidy_title(p['title'])
        num = max_num + 1 + len(added)
        slug = f"{num:03d}-{slugify(p['title'])}"
        dest = os.path.join(IMG_DIR, slug + '.webp')
        if os.path.exists(dest) or not dl(p['full'], dest):
            print(f"  ! download failed, skipping: {p['title']}")
            continue
        w, h = image_dims(dest, (p['ar_w'], p['ar_h']))
        added.append({
            'id': slug, 'title': p['title'], 'caption': p['caption'],
            'alt': p['alt'] or p['caption'][:160],
            'date': p['date'], 'time': p['time'], 'fileId': p['fileId'],
            'tags': p['tags'][:8], 'src': f"/images/{slug}.webp",
            'w': w, 'h': h, 'series': p.get('_series_override') or classify(p),
            'bskyUrl': p['bskyUrl'],
        })

    if not added:
        print("All new posts failed to download — nothing changed.")
        return

    photos = added + photos                    # newest-first, prepended
    json.dump(photos, open(CLEAN, 'w'), indent=1, ensure_ascii=False)
    state['seen_rkeys'] = sorted(set(state['seen_rkeys']) | {p['bskyUrl'].rsplit('/', 1)[-1] for p in new})[:2000]
    state['seen_cids'] = sorted(set(state['seen_cids']) | {p['cid'] for p in new})[:2000]
    json.dump(state, open(STATE, 'w'), indent=1)

    subprocess.run([sys.executable, os.path.join(SCRIPTS, 'gen_ts.py')], check=True)

    print(f"\nAdded {len(added)} new photograph(s):")
    for p in added:
        print(f"  {p['id']}  [{p['series']}]  {p['title']}  ({p['date']})")
    print("Series distribution:", Counter(p['series'] for p in photos))

if __name__ == '__main__':
    main()
