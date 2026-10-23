#!/usr/bin/env python3
"""One-off maintenance: re-sort photos_clean.json strictly date-desc.

Same-date ties keep the original relative order (lower archival number =
posted earlier in that day's feed sequence = newer position).
"""
import json, re

PATH = '/home/z/my-project/scripts/photos_clean.json'
photos = json.load(open(PATH))

def key(p):
    m = re.match(r'^(\d{3})-', p['id'])
    num = int(m.group(1)) if m else 999
    # date desc, then archival number asc within the same date
    return (tuple(-int(x) for x in p['date'].split('-')), num)

photos.sort(key=key)
json.dump(photos, open(PATH, 'w'), indent=1, ensure_ascii=False)
print(f"re-sorted {len(photos)} photos")
print("newest 3:", [(p['id'], p['date']) for p in photos[:3]])
print("oldest 3:", [(p['id'], p['date']) for p in photos[-3:]])
