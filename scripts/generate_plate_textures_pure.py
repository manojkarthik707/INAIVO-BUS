"""
generate_plate_textures_pure.py — Generate 100 license plate PNG/BMP textures.
Uses ONLY stdlib (struct, zlib) — no external dependencies.
Writes uncompressed BMP files that Webots can load as ImageTexture.
"""

import struct
import os

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


# ===== Minimal 8x8 pixel font for A-Z, 0-9, space =====
# Each char is 8 columns x 8 rows, stored as 8 bytes (one byte per row, MSB=leftmost pixel)
FONT = {
    ' ': [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
    '0': [0x3C,0x66,0x6E,0x76,0x66,0x66,0x3C,0x00],
    '1': [0x18,0x38,0x18,0x18,0x18,0x18,0x7E,0x00],
    '2': [0x3C,0x66,0x06,0x1C,0x30,0x66,0x7E,0x00],
    '3': [0x3C,0x66,0x06,0x1C,0x06,0x66,0x3C,0x00],
    '4': [0x0C,0x1C,0x3C,0x6C,0x7E,0x0C,0x0C,0x00],
    '5': [0x7E,0x60,0x7C,0x06,0x06,0x66,0x3C,0x00],
    '6': [0x1C,0x30,0x60,0x7C,0x66,0x66,0x3C,0x00],
    '7': [0x7E,0x66,0x0C,0x18,0x18,0x18,0x18,0x00],
    '8': [0x3C,0x66,0x66,0x3C,0x66,0x66,0x3C,0x00],
    '9': [0x3C,0x66,0x66,0x3E,0x06,0x0C,0x38,0x00],
    'A': [0x18,0x3C,0x66,0x7E,0x66,0x66,0x66,0x00],
    'B': [0x7C,0x66,0x66,0x7C,0x66,0x66,0x7C,0x00],
    'C': [0x3C,0x66,0x60,0x60,0x60,0x66,0x3C,0x00],
    'D': [0x78,0x6C,0x66,0x66,0x66,0x6C,0x78,0x00],
    'E': [0x7E,0x60,0x60,0x78,0x60,0x60,0x7E,0x00],
    'F': [0x7E,0x60,0x60,0x78,0x60,0x60,0x60,0x00],
    'G': [0x3C,0x66,0x60,0x6E,0x66,0x66,0x3C,0x00],
    'H': [0x66,0x66,0x66,0x7E,0x66,0x66,0x66,0x00],
    'I': [0x3C,0x18,0x18,0x18,0x18,0x18,0x3C,0x00],
    'J': [0x1E,0x0C,0x0C,0x0C,0x0C,0x6C,0x38,0x00],
    'K': [0x66,0x6C,0x78,0x70,0x78,0x6C,0x66,0x00],
    'L': [0x60,0x60,0x60,0x60,0x60,0x60,0x7E,0x00],
    'M': [0x63,0x77,0x7F,0x6B,0x63,0x63,0x63,0x00],
    'N': [0x66,0x76,0x7E,0x7E,0x6E,0x66,0x66,0x00],
    'P': [0x7C,0x66,0x66,0x7C,0x60,0x60,0x60,0x00],
    'Q': [0x3C,0x66,0x66,0x66,0x6E,0x3C,0x06,0x00],
    'R': [0x7C,0x66,0x66,0x7C,0x78,0x6C,0x66,0x00],
    'S': [0x3C,0x66,0x60,0x3C,0x06,0x66,0x3C,0x00],
    'T': [0x7E,0x18,0x18,0x18,0x18,0x18,0x18,0x00],
    'U': [0x66,0x66,0x66,0x66,0x66,0x66,0x3C,0x00],
    'V': [0x66,0x66,0x66,0x66,0x66,0x3C,0x18,0x00],
    'W': [0x63,0x63,0x63,0x6B,0x7F,0x77,0x63,0x00],
    'X': [0x66,0x66,0x3C,0x18,0x3C,0x66,0x66,0x00],
    'Y': [0x66,0x66,0x3C,0x18,0x18,0x18,0x18,0x00],
    'Z': [0x7E,0x06,0x0C,0x18,0x30,0x60,0x7E,0x00],
}

SCALE = 4  # Scale each 8x8 glyph to 32x32 px


def write_bmp(path, pixels, w, h):
    """Write uncompressed 24-bit BMP. pixels is list of (r,g,b) tuples, row-major top-to-bottom."""
    row_size = ((w * 3 + 3) // 4) * 4  # BMP rows are 4-byte aligned
    pixel_data_size = row_size * h
    file_size = 54 + pixel_data_size

    bmp = bytearray()
    # File header
    bmp += b'BM'
    bmp += struct.pack('<I', file_size)
    bmp += struct.pack('<HH', 0, 0)
    bmp += struct.pack('<I', 54)
    # DIB header
    bmp += struct.pack('<I', 40)         # header size
    bmp += struct.pack('<i', w)
    bmp += struct.pack('<i', -h)         # negative = top-down
    bmp += struct.pack('<H', 1)          # color planes
    bmp += struct.pack('<H', 24)         # bits per pixel
    bmp += struct.pack('<I', 0)          # no compression
    bmp += struct.pack('<I', pixel_data_size)
    bmp += struct.pack('<i', 2835)       # 72 DPI
    bmp += struct.pack('<i', 2835)
    bmp += struct.pack('<I', 0)
    bmp += struct.pack('<I', 0)

    for row in range(h):
        row_bytes = bytearray()
        for col in range(w):
            r, g, b = pixels[row * w + col]
            row_bytes += bytes([b, g, r])  # BMP stores BGR
        # Pad to 4-byte boundary
        pad = row_size - len(row_bytes)
        row_bytes += bytes(pad)
        bmp += row_bytes

    with open(path, 'wb') as f:
        f.write(bmp)


def render_text(text, scale=SCALE):
    """Render text using bitmap font. Returns (pixel_rows list of rows, w, h)."""
    chars = list(text)
    gap = 1  # pixel gap between chars
    total_cols = len(chars) * (8 + gap) * scale
    total_rows = 8 * scale
    pixels = [(245, 245, 235)] * (total_cols * total_rows)

    for ci, ch in enumerate(chars):
        glyph = FONT.get(ch.upper(), FONT[' '])
        for row in range(8):
            byte = glyph[row]
            for col in range(8):
                bit = (byte >> (7 - col)) & 1
                color = (10, 10, 10) if bit else (245, 245, 235)
                for sr in range(scale):
                    for sc in range(scale):
                        px = (row * scale + sr) * total_cols + ci * (8 + gap) * scale + col * scale + sc
                        pixels[px] = color

    return pixels, total_cols, total_rows


def make_plate_image(plate_str, img_w=520, img_h=115):
    """Create full plate image with white background, border, IND stripe, plate text."""
    pixels = [(245, 245, 235)] * (img_w * img_h)

    # Yellow IND stripe top
    stripe_h = 18
    for row in range(stripe_h):
        for col in range(img_w):
            pixels[row * img_w + col] = (255, 204, 0)

    # Border (4px)
    for row in range(img_h):
        for col in range(img_w):
            if row < 4 or row >= img_h-4 or col < 4 or col >= img_w-4:
                pixels[row * img_w + col] = (50, 50, 50)

    # Render plate text
    text_pixels, tw, th = render_text(plate_str, scale=SCALE)
    x_off = (img_w - tw) // 2
    y_off = stripe_h + (img_h - stripe_h - th) // 2
    x_off = max(5, x_off)
    y_off = max(stripe_h + 2, y_off)

    for row in range(min(th, img_h - y_off - 4)):
        for col in range(min(tw, img_w - x_off - 4)):
            src = text_pixels[row * tw + col]
            if src == (10, 10, 10):  # dark pixel
                pixels[(y_off + row) * img_w + (x_off + col)] = src

    return pixels, img_w, img_h


# Generate all 100 plates
for i in range(100):
    plate_str = get_plate(i)
    pixels, w, h = make_plate_image(plate_str)
    out_path = os.path.join(PLATES_DIR, f"plate_{i:03d}.bmp")
    write_bmp(out_path, pixels, w, h)
    if i % 20 == 0:
        print(f"  Generated {i}/100: {plate_str}")

print(f"Done. 100 BMP plate textures written to {PLATES_DIR}")
