import json

with open('/home/z/my-project/scripts/bsky_feed_raw.json') as f:
    wrapper = json.load(f)

# wrapper: {success, data, error}; data should be the JSON string of the API response
data = wrapper['data']
if isinstance(data, dict) and 'result' in data:
    data = data['result']
if isinstance(data, str):
    data = json.loads(data)

feed = data.get('feed', [])
print(f"Total posts retrieved: {len(feed)}\n" + "=" * 70)

for i, item in enumerate(feed, 1):
    post = item.get('post', {})
    record = post.get('record', {})
    text = record.get('text', '').strip()
    created = record.get('createdAt', '')[:10]
    embed = post.get('embed', {})
    has_img = False
    alt = ''
    # images
    if embed.get('$type') == 'app.bsky.embed.images#view':
        imgs = embed.get('images', [])
        if imgs:
            has_img = True
            alt = imgs[0].get('alt', '')
    elif embed.get('$type') == 'app.bsky.embed.external#view':
        has_img = True
        alt = '[external link]'
    if not has_img and record.get('embed'):
        e = record['embed']
        if isinstance(e, dict) and 'images' in e:
            has_img = True
            alts = [im.get('alt', '') for im in e['images']]
            alt = ' | '.join(a for a in alts if a)
    imgs_alt_note = 'IMG' if has_img else 'txt'
    print(f"\n--- #{i} [{imgs_alt_note}] {created} ---")
    print(text)
    if alt and alt != '[external link]':
        print(f"[ALT: {alt}]")

# profile info
prof = data.get('profile', {})
