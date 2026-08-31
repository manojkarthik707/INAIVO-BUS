import re
from PIL import Image

# 1. Resize custom_signboard_logo.png to exact power-of-two 2048x2048
TEX_PATH = r"f:\VEHDEMO\simulation\webots\worlds\textures\custom_signboard_logo.png"
img = Image.open(TEX_PATH)
img_resized = img.resize((2048, 2048), Image.Resampling.LANCZOS)
img_resized.save(TEX_PATH, format="PNG")
img_resized.save(r"f:\VEHDEMO\frontend\public\custom_signboard_logo.png", format="PNG")
print(f"Resized {TEX_PATH} to exact power-of-two (2048x2048)")

# 2. Fix AdvertisingBoard names in sih_mvp_traffic.wbt
WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"
with open(WBT_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

board_count = 0
def name_advertising_board(m):
    global board_count
    board_count += 1
    block = m.group(0)
    # Remove existing name line if present
    block = re.sub(r'name\s*"[^"]*"\s*\n?', '', block)
    # Add unique name
    replacement = f'name "inetra_billboard_{board_count}"\n'
    return block.replace('AdvertisingBoard {', f'AdvertisingBoard {{\n  {replacement}')

content = re.sub(r'AdvertisingBoard\s*\{[^}]*\}', name_advertising_board, content)

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Assigned unique names to all {board_count} AdvertisingBoard nodes in {WBT_PATH}")
