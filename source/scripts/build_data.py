#!/usr/bin/env python3
"""Pipeline: Bluesky feed JSON -> local images + src/data/photos.ts"""
import json, re, os, subprocess, unicodedata

BASE = '/home/z/my-project'
IMG_DIR = os.path.join(BASE, 'public', 'images')
os.makedirs(IMG_DIR, exist_ok=True)

with open(os.path.join(BASE, 'scripts', 'bsky_feed_raw.json')) as f:
    wrapper = json.load(f)
data = wrapper['data']
if isinstance(data, dict) and 'result' in data:
    data = data['result']
if isinstance(data, str):
    data = json.loads(data)

feed = data.get('feed', [])

def clean_text(t):
    return (t or '').replace('\u00a0', ' ').strip()

def slugify(s, maxlen=42):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode()
    s = re.sub(r"[^a-zA-Z0-9]+", '-', s).strip('-').lower()
    return s[:maxlen].rstrip('-') or 'untitled'

# ---------- parsing helpers ----------
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
    img = images[0]
    full = img.get('fullsize', '')
    alt = clean_text(img.get('alt', ''))
    rkey = post.get('uri', '').split('/')[-1]
    created = rec.get('createdAt', '')[:10]
    if not full:
        return None

    lines = [l.strip() for l in text.split('\n')]

    # title: quoted string on first line(s), or Title: X (anywhere)
    title = ''
    m = re.match(r'^(?:Photo[:\s]*)?["\u201c\u201d]([^"\u201c\u201d]+)["\u201c\u201d]', text)
    if m:
        title = m.group(1).strip()
    else:
        m = re.search(r'Title\s*[:=]\s*["\u201c]?\s*([^"\u201c\u201d\n]{3,80})', text, re.I)
        if m:
            title = m.group(1).strip().strip('"').strip()

    # image CID for dedupe
    cid = full.rsplit('/', 1)[-1]

    # fileId
    fm = re.search(r'\bID[:=]\s*([A-Za-z0-9_.\-]+)', text)
    file_id = fm.group(1).strip().rstrip('.,') if fm else ''

    # time
    tm = re.search(r'\bTime[s]?:\s*([0-9]{1,2}:[0-9]{2}(?::[0-9]{2})?)', text)
    time_s = tm.group(1) if tm else ''

    # tags
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
        if re.match(r'^(ID|Id|id)[:=]', l) or re.match(r'^\s*Time[s]?\s*[:\s]', l) or re.match(r'^(Hours?|Captured|Date|Original size|Size|Raw and DNG|Photo and post)', l, re.I):
            continue
        if l.startswith('#'):
            continue
        if re.match(r'^Photo by', l, re.I) or re.match(r'^@dadasese69', l, re.I):
            continue
        keep.append(l)
    cap = '\n'.join(keep)
    cap = re.sub(r'\n{3,}', '\n\n', cap).strip(' \n\t-')
    # trailing dangling quotes
    cap = cap.strip()
    if not title:
        first = [l for l in lines if l and not l.startswith('#')]
        title = (first[0][:48] if first else f'Untitled {idx}')
        title = title.strip('"')

    return {
        'rkey': rkey, 'title': title, 'caption': cap, 'alt': alt,
        'date': created, 'time': time_s, 'fileId': file_id, 'tags': tags,
        'full': full, 'cid': cid, 'bskyUrl': f"https://bsky.app/profile/dadasese69.bsky.social/post/{rkey}",
    }

parsed, seen = [], set()
for item in feed:
    p = parse_post(item, len(parsed) + 1)
    if not p:
        continue
    if p['rkey'] in seen:
        continue
    seen.add(p['rkey'])
    parsed.append(p)

# dedupe identical images (same CID), drop announcements
seen_cid, deduped = set(), []
for p in parsed:
    if p.get('cid') in seen_cid:
        continue
    seen_cid.add(p.get('cid'))
    if p['date'] == '2025-07-11':      # LensCulture announcement -> About page instead
        continue
    deduped.append(p)
parsed = deduped

# newest first
parsed.sort(key=lambda p: p['date'], reverse=True)
print(f"Image posts to import: {len(parsed)}")

# manual curatorial fixes: (date, title-prefix) -> (title, series)
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
    ('2025-03-03', 'A world without birds'):( 'A world without birds', 'witnesses'),
}
def apply_manual(p):
    for (d, pref), (t, s) in MANUAL.items():
        if p['date'] == d and p['title'].startswith(pref):
            p['title'], p['_series_override'] = t, s
            return

# clean titles of extracted header junk
def tidy_title(t):
    t = re.sub(r'^(Time[s]?|Date|Hours?)\s*[:\s].*$', '', t).strip()
    return t or 'Untitled'

# ---------- series classification ----------
WIT = r'\b(heron|pigeon|crow|gull|seagull|swan|starling|duck|bird|cat|dog|sparrow|magpie|owl|wings?|feather|animal|oxen|snake|turtle|fish)\b'
BILD = r'\b(skyscraper|tower|scaffold|glass|facade|architecture|duomo|construction|building|buildings|contrail|skyline)\b'
OVERRIDES = {   # title.lower() substring -> series
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

# ---------- download ----------
def dl(url, dest):
    for i in range(3):
        r = subprocess.run(['curl', '-sL', '--max-time', '60', '-o', dest, url],
                           capture_output=True)
        if r.returncode == 0 and os.path.exists(dest) and os.path.getsize(dest) > 5000:
            return True
    return False

try:
    from PIL import Image
    HAS_PIL = True
except Exception:
    HAS_PIL = False

photos = []
failed = []
for i, p in enumerate(parsed, 1):
    apply_manual(p)
    p['title'] = tidy_title(p['title'])
    slug = f"{i:03d}-{slugify(p['title'])}"
    dest = os.path.join(IMG_DIR, slug + '.webp')
    if not os.path.exists(dest):
        if not dl(p['full'], dest):
            failed.append(p['title']); continue
    w = h = 0
    if HAS_PIL:
        try:
            with Image.open(dest) as im:
                w, h = im.size
        except Exception:
            pass
    photos.append({
        'id': slug, 'title': p['title'], 'caption': p['caption'], 'alt': p['alt'] or p['caption'][:160],
        'date': p['date'], 'time': p['time'], 'fileId': p['fileId'],
        'tags': p['tags'][:8], 'src': f"/images/{slug}.webp",
        'w': w, 'h': h, 'series': p.get('_series_override') or classify(p), 'bskyUrl': p['bskyUrl'],
    })

print(f"Downloaded: {len(photos)}  Failed: {len(failed)} {failed[:5]}")
from collections import Counter
print("Series distribution:", Counter(p['series'] for p in photos))

# avatar
av = None
if feed:
    av = feed[0].get('post', {}).get('author', {}).get('avatar')
if av:
    ok = dl(av, os.path.join(IMG_DIR, 'avatar.webp'))
    print('avatar:', 'ok' if ok else 'FAILED', av)

with open(os.path.join(BASE, 'scripts', 'photos_clean.json'), 'w') as f:
    json.dump(photos, f, indent=1, ensure_ascii=False)
print("saved photos_clean.json")
