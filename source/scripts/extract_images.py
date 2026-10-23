import json

with open('/home/z/my-project/scripts/bsky_feed_raw.json') as f:
    wrapper = json.load(f)

data = wrapper['data']
if isinstance(data, dict) and 'result' in data:
    data = data['result']
if isinstance(data, str):
    data = json.loads(data)

feed = data.get('feed', [])

# Extract post url + fullsize image url for key emblematic posts
targets = ['Fence to face', 'Bulb Stars', 'Noble gas', 'Curved dot', 'The Hero', 'A world without birds',
           'Three Trees', 'This is Oxford', 'Price of Rain', 'Signed By The Air', 'Windowsill', 'splash', 'Turn around']

out = []
for item in feed:
    post = item.get('post', {})
    rec = post.get('record', {})
    text = rec.get('text', '')
    rkey = post.get('uri', '').split('/')[-1]
    embed = post.get('embed', {})
    urls = []
    if embed.get('$type') == 'app.bsky.embed.images#view':
        for im in embed.get('images', []):
            fu = im.get('fullsize', '')
            if fu:
                urls.append(fu)
    title_hit = [t for t in targets if t.lower() in text.lower()]
    if urls and title_hit:
        for u in urls:
            out.append((title_hit[0], rkey, u))

for t, rk, u in out:
    print(f"{t} | https://bsky.app/profile/dadasese69.bsky.social/post/{rk} | {u}")
