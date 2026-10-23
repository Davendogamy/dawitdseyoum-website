#!/usr/bin/env python3
"""Generate src/data/photos.ts from photos_clean.json
(portable paths — runnable locally and in GitHub Actions)"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
photos = json.load(open(os.path.join(ROOT, 'scripts', 'photos_clean.json')))

TS = '''// AUTO-GENERATED from the artist's Bluesky feed (dadasese69.bsky.social)
// Auto-refreshed daily by scripts/sync_bluesky.py (GitHub Actions) — do not edit by hand

export type SeriesId = 'witnesses' | 'builders' | 'commons'

export interface Photo {
  id: string
  title: string
  caption: string
  alt: string
  date: string
  time: string
  fileId: string
  tags: string[]
  src: string
  w: number
  h: number
  series: SeriesId
  bskyUrl: string
}

export const seriesMeta: Record<SeriesId, {
  name: string
  tagline: string
  note: string
  bg: string
}> = {
  witnesses: {
    name: 'The Witnesses',
    tagline: 'Birds and animals, residents of the city',
    note: 'The heron, the crow, the pigeon, the swan — they were here before the glass arrived, and they refuse to leave. They watch; they speak. Every caption is their testimony, witnessed and transcribed by the photographer.',
    bg: '#0f1d28',
  },
  builders: {
    name: 'The Builders',
    tagline: 'Cranes, scaffolds and towers',
    note: 'The geometry of progress: concrete poured over meadow, glass answering the sky, cranes asking why reach for the universe by piling stone upon stone. Development is not the enemy here — it is a character, studied closely.',
    bg: '#10222b',
  },
  commons: {
    name: 'The Commons',
    tagline: 'Parks, water, streets and skies',
    note: 'The shared grounds where city and nature negotiate daily: a fountain, a smoggy sunrise, a mock strawberry, a bench aging in queue. The ordinary places where resilience persists — delicate, deliberate, alive.',
    bg: '#0e1a22',
  },
}

export const CONTACT_EMAIL = 'dawit.seyoum@gmail.com'

export const SOCIALS = [
  { name: 'Bluesky', url: 'https://bsky.app/profile/dadasese69.bsky.social' },
  { name: 'Instagram', url: 'https://instagram.com/dadasese69' },
  { name: 'Pixelfed', url: 'https://pixelfed.social/dadasese69' },
  { name: 'Flickr', url: 'https://www.flickr.com/photos/dadasese69' },
]

export const photos: Photo[] = [
'''

def esc(s):
    return json.dumps(s, ensure_ascii=False)

for p in photos:
    TS += '  {\n'
    TS += f'    id: {esc(p["id"])},\n'
    TS += f'    title: {esc(p["title"])},\n'
    TS += f'    caption: {esc(p["caption"])},\n'
    TS += f'    alt: {esc(p["alt"])},\n'
    TS += f'    date: {esc(p["date"])},\n'
    TS += f'    time: {esc(p["time"])},\n'
    TS += f'    fileId: {esc(p["fileId"])},\n'
    TS += f'    tags: {json.dumps(p["tags"], ensure_ascii=False)},\n'
    TS += f'    src: {esc(p["src"])},\n'
    TS += f'    w: {p["w"]}, h: {p["h"]},\n'
    TS += f'    series: {esc(p["series"])} as SeriesId,\n'
    TS += f'    bskyUrl: {esc(p["bskyUrl"])},\n'
    TS += '  },\n'

TS += ']\n'

with open(os.path.join(ROOT, 'src', 'data', 'photos.ts'), 'w') as f:
    f.write(TS)
print(f'Wrote src/data/photos.ts ({len(photos)} entries, {len(TS)/1024:.0f} KB)')
