"""
generate_plate_textures.py — Pre-generate 100 unique Indian license plate PNG textures.

Generates 1024x128 power-of-2 plate images (no Webots rescaling warning).
Saves to simulation/webots/worlds/textures/plates/plate_NNN.png
"""

import os
from PIL import Image, ImageDraw, ImageFont

PLATES_DIR = r"f:\VEHDEMO\simulation\webots\worlds\textures\plates"
os.makedirs(PLATES_DIR, exist_ok=True)

INDIAN_STATES = ["TN", "KA", "MH", "DL", "TS", "GJ", "KL", "AP", "WB", "HR"]
SERIES = ["AB", "CD", "EF", "GH", "JK", "LM", "NP", "QR", "ST", "UV", "WX", "YZ"]

def get_plate(v_idx):
    state = INDIAN_STATES[v_idx % len(INDIAN_STATES)]
    rto = f"{(v_idx * 3 + 1) % 99 + 1:02d}"
    series = SERIES[(v_idx // len(INDIAN_STATES)) % len(SERIES)]
    num = f"{(v_idx * 127 + 1001) % 9000 + 1000:04d}"
    return f"{state} {rto} {series} {num}"

# Power-of-2 dimensions — no Webots WARNING
W, H = 1024, 128

# Load bold font — large enough for 1024px wide plate
font_big  = None
font_small = None
BOLD_FONT = "C:/Windows/Fonts/arialbd.ttf"
NORMAL_FONT = "C:/Windows/Fonts/arial.ttf"
for font_path in [BOLD_FONT, NORMAL_FONT, "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
    if os.path.exists(font_path):
        font_big   = ImageFont.truetype(font_path, 78)
        font_small = ImageFont.truetype(font_path, 16)
        break
if font_big is None:
    font_big = font_small = ImageFont.load_default()

STRIPE_H = 22  # yellow IND stripe height
BORDER   = 5

for i in range(100):
    plate_str = get_plate(i)
    img = Image.new("RGB", (W, H), color=(245, 245, 235))
    draw = ImageDraw.Draw(img)

    # Yellow IND stripe at top
    draw.rectangle([0, 0, W, STRIPE_H], fill=(255, 200, 0))
    draw.text((W // 2 - 18, 3), "IND", fill=(0, 0, 120), font=font_small)

    # Dark border
    draw.rectangle([0, 0, W - 1, H - 1], outline=(40, 40, 40), width=BORDER)
    draw.line([(0, STRIPE_H), (W, STRIPE_H)], fill=(80, 80, 80), width=2)

    # Center plate number text
    bbox = draw.textbbox((0, 0), plate_str, font=font_big)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (W - tw) // 2
    y = STRIPE_H + (H - STRIPE_H - th) // 2 - 4
    draw.text((x, y), plate_str, fill=(10, 10, 10), font=font_big)

    out_path = os.path.join(PLATES_DIR, f"plate_{i:03d}.png")
    img.save(out_path, optimize=True)

print(f"Generated 100 plate PNGs (1024x128, power-of-2) in {PLATES_DIR}")
