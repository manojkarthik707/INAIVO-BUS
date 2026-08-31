"""
generate_plate_textures.py — Pre-generate 100 unique Indian license plate PNG textures.

Generates white 520x115 px plate images with bold black text.
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

W, H = 520, 115

# Try to load a bold font; fallback to built-in
font = None
for font_path in [
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/calibrib.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]:
    if os.path.exists(font_path):
        font = ImageFont.truetype(font_path, 62)
        break
if font is None:
    font = ImageFont.load_default()

for i in range(100):
    plate_str = get_plate(i)
    img = Image.new("RGB", (W, H), color=(245, 245, 235))
    draw = ImageDraw.Draw(img)

    # Draw yellow top stripe (IND)
    draw.rectangle([0, 0, W, 18], fill=(255, 204, 0))
    draw.text((W//2 - 20, 0), "IND", fill=(0, 0, 100), font=ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 14) if os.path.exists("C:/Windows/Fonts/arialbd.ttf") else font)

    # Draw border
    draw.rectangle([0, 0, W-1, H-1], outline=(50, 50, 50), width=4)

    # Draw plate text centered
    bbox = draw.textbbox((0, 0), plate_str, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (W - tw) // 2
    y = 22 + (H - 22 - th) // 2
    draw.text((x, y), plate_str, fill=(10, 10, 10), font=font)

    out_path = os.path.join(PLATES_DIR, f"plate_{i:03d}.png")
    img.save(out_path)

print(f"Generated 100 plate PNGs in {PLATES_DIR}")
