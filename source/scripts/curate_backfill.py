#!/usr/bin/env python3
"""One-off editorial curation of the 14 backfilled works (sync backfill, Oct 2026).

Applies the same curation standards as the founding collection:
- titles come from the artist's own words, shortened to wall-label length
- pure @handle mentions are not titles/captions
- non-artwork posts (platform milestone screenshot) are excluded
- series assignment follows the motif logic (The Witnesses / The Builders / The Commons)
"""
import json, re, os

ROOT = '/home/z/my-project'
CLEAN = os.path.join(ROOT, 'scripts', 'photos_clean.json')
RAW = os.path.join(ROOT, 'scripts', 'bsky_feed_raw.json')

photos = json.load(open(CLEAN))
by_id = {p['id']: p for p in photos}

# ---- 091: recover the real caption from the raw feed (the 'Captured' prefix
#          regex ate it as if it were metadata), title from his own words
raw = json.load(open(RAW))
def full_text(bsky_url):
    rkey = bsky_url.rsplit('/', 1)[-1]
    for item in raw.get('feed', []):
        if item.get('post', {}).get('uri', '').endswith(rkey):
            return item['post']['record'].get('text', '')
    return ''

# ---- direct edits: id -> fields ----
EDITS = {
    '091-captured-at-a-quiet-6-a-m-where-the-interp': {'title': 'Quiet, 6 a.m.'},
    '093-nature-s-palette-ducks-in-a-blue-hued-rive': {'series': 'witnesses'},
    '094-skyline-moments-where-colors-blend-and-ser': {'title': 'Skyline moments', 'series': 'witnesses'},
    '096-sunrise-blooms-on-mother-s-day-may-8th-202':  {'title': "Sunrise blooms on Mother's Day, May 8th 2024."},
    '098-one-winter-evening-cold-and-misty-i-went-o':  {'title': 'One winter evening'},
    '099-streetphotography-bsky-social':               {'title': 'Street crossing, Milan', 'caption': ''},
    '100-i-could-not-keep-this-photo-with-me-i-have':  {'title': 'Laika', 'series': 'witnesses'},
    '101-streetphotography-bsky-social':               {'title': 'Morning walk, Bosco Verticale', 'caption': '', 'series': 'builders'},
    '102-nested-within-the-towering-skyscrapers-of':   {'title': 'A playground oasis'},
    '103-nestled-within-the-storied-streets-of-oxfo':  {'title': 'Storied streets'},
}

EXCLUDE = ['092-bluesky-now-has-over-10-million-users-and']   # milestone screenshot, not artwork

for pid, fields in EDITS.items():
    p = by_id[pid]
    for k, v in fields.items():
        p[k] = v
    if pid.startswith('091'):
        txt = full_text(p['bskyUrl'])
        prose = [l.strip() for l in txt.split('\n')
                 if l.strip() and not l.strip().startswith('#')]
        p['caption'] = prose[0] if prose else ''
        p['alt'] = p['caption']

for pid in EXCLUDE:
    photos = [p for p in photos if p['id'] != pid]
    f = os.path.join(ROOT, 'public', 'images', pid + '.webp')
    if os.path.exists(f):
        os.remove(f)

# ---- re-sort strictly date-desc (same-date ties: archival number asc) ----
def key(p):
    m = re.match(r'^(\d{3})-', p['id'])
    num = int(m.group(1)) if m else 999
    return (tuple(-int(x) for x in p['date'].split('-')), num)

photos.sort(key=key)
json.dump(photos, open(CLEAN, 'w'), indent=1, ensure_ascii=False)
print(f"curated: {len(photos)} photos (excluded {len(EXCLUDE)})")
from collections import Counter
print("series:", dict(Counter(p['series'] for p in photos)))
for p in photos[:2]:
    print("  newest:", p['id'], p['date'])
