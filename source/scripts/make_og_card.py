#!/usr/bin/env python3
"""Generate public/og-card.jpg — the 1200x630 social share card.

Museum wall-label aesthetic matching the site palette:
  ink wall #0b131b / bone white #e8e4da / red accent #c5402f
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (11, 19, 27)        # #0b131b ink wall
BONE = (232, 228, 218)   # #e8e4da bone white
MUTED = (146, 160, 170)  # quiet steel for secondary lines
RED = (197, 64, 47)      # #c5402f — the living accent

TINOS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
MONO = "/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf"

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# --- hairline frame (museum matte) ---
inset = 30
d.rectangle([inset, inset, W - inset, H - inset], outline=(60, 74, 85), width=1)
inset2 = 38
d.rectangle([inset2, inset2, W - inset2, H - inset2], outline=(38, 50, 60), width=1)


def draw_tracked(draw, cx, cy, text, font, tracking, fill):
    """Draw text centered at (cx, cy) with per-glyph letter spacing."""
    widths = [font.getlength(ch) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    asc, desc = font.getmetrics()
    y = cy - (asc + desc) / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + tracking
    return total


f_name = ImageFont.truetype(TINOS, 78)
f_sub = ImageFont.truetype(MONO, 23)
f_url = ImageFont.truetype(MONO, 19)

# --- artist name ---
draw_tracked(d, W / 2, 248, "DAWIT D. SEYOUM", f_name, 7, BONE)

# --- red dot (the site's living accent) ---
dot_r = 5
d.ellipse(
    [W / 2 - dot_r, 336 - dot_r, W / 2 + dot_r, 336 + dot_r],
    fill=RED,
)

# --- subtitle ---
draw_tracked(
    d, W / 2, 392,
    "EYE IN THE CITY  \u00b7  FINE ART PHOTOGRAPHY",
    f_sub, 5, MUTED,
)

# --- domain, quiet, near the bottom frame ---
draw_tracked(d, W / 2, 540, "DAWITDSEYOUM.COM", f_url, 6, (110, 124, 135))

out = "/home/z/my-project/public/og-card.jpg"
img.save(out, "JPEG", quality=92, optimize=True)
print("saved", out)
