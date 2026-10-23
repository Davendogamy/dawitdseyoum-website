#!/bin/bash
# Build dawitdseyoum-selfsync-upgrade.zip — drop-in package for the user's
# static GitHub repo (dawitdseyoum-website) that adds the Bluesky self-sync
# engine + GitHub Action. Repo root stays the live static site (served by
# Cloudflare); source/ is the workshop; .github/workflows runs daily.
set -euo pipefail

BASE=/home/z/my-project
ASSETS=$BASE/scripts/selfsync_assets
STAGE=$BASE/selfsync-stage
ZIP=$BASE/download/dawitdseyoum-selfsync-upgrade.zip

echo "== 1. staging lean source tree =="
rm -rf "$STAGE"
mkdir -p "$STAGE/source" "$STAGE/.github/workflows"

cd "$BASE"
rsync -a \
  --exclude 'node_modules' \
  --exclude '.next' \
  --exclude 'out' \
  --exclude 'db' \
  --exclude 'examples' \
  --exclude 'tests' \
  --exclude 'download' \
  --exclude 'selfsync-stage' \
  --exclude 'Caddyfile' \
  --exclude 'worklog.md' \
  --exclude 'bun.lock' \
  --exclude 'dev.log' \
  --exclude 'server.log' \
  --exclude 'img_*.jpg' \
  --exclude 'img_*.webp' \
  --exclude 'scripts/verify_*.png' \
  --exclude 'scripts/img_*.webp' \
  --exclude 'scripts/img_*.jpg' \
  --exclude 'scripts/bsky_feed_raw.json' \
  --exclude 'scripts/bsky_captions.txt' \
  --exclude 'scripts/selfsync_assets' \
  src public prisma scripts package.json next.config.ts tsconfig.json postcss.config.mjs tailwind.config.ts components.json eslint.config.mjs \
  "$STAGE/source/"

cp "$ASSETS/self-sync.yml"      "$STAGE/.github/workflows/self-sync.yml"
cp "$ASSETS/gitignore"          "$STAGE/.gitignore"
cp "$ASSETS/assetsignore"       "$STAGE/.assetsignore"
cp "$ASSETS/UPDATE-README.txt"  "$STAGE/UPDATE-README.txt"

echo "== 2. staged pipeline test (path-portability + Bluesky reach) =="
cd "$STAGE/source"
python3 scripts/sync_bluesky.py

echo "== 3. packaging =="
rm -f "$ZIP"
cd "$STAGE"
zip -qr "$ZIP" .github source .gitignore .assetsignore UPDATE-README.txt

echo "---- verification ----"
unzip -l "$ZIP" | head -6
unzip -l "$ZIP" | tail -4
echo "key files present:"
unzip -l "$ZIP" | grep -E 'self-sync.yml|sync_bluesky.py|photos_clean.json|sync_state.json|photos.ts|UPDATE-README|gitignore|assetsignore' || true
echo "image count in package:"
unzip -l "$ZIP" | grep -c 'public/images/.*webp' || true
du -h "$ZIP"
