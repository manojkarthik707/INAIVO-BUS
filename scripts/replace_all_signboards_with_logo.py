import re
import shutil
import os

LOGO_SRC = r"f:\VEHDEMO\simulation\webots\worlds\textures\custom_signboard_logo.png"
WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"

# Ensure textures directory exists
os.makedirs(r"f:\VEHDEMO\simulation\webots\worlds\textures", exist_ok=True)
os.makedirs(r"f:\VEHDEMO\frontend\public", exist_ok=True)
shutil.copy(LOGO_SRC, r"f:\VEHDEMO\frontend\public\custom_signboard_logo.png")

with open(WBT_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace all highway sign textures with custom logo
content = re.sub(
    r'texture\s*\[\s*"[^"]*highway_sign_[^"]*\.jpg"\s*\]',
    'texture [ "textures/custom_signboard_logo.png" ]',
    content
)

# 2. Update all AdvertisingBoard nodes with frontTexture and backTexture
def update_advertising_board(m):
    block = m.group(0)
    # Remove existing front/back texture lines
    block = re.sub(r'frontTexture\s*\[[^\]]*\]', '', block)
    block = re.sub(r'backTexture\s*\[[^\]]*\]', '', block)
    
    # Insert new front and back texture
    replacement = 'frontTexture [ "textures/custom_signboard_logo.png" ]\n  backTexture [ "textures/custom_signboard_logo.png" ]\n'
    return block.replace('AdvertisingBoard {', f'AdvertisingBoard {{\n  {replacement}')

content = re.sub(r'AdvertisingBoard\s*\{[^}]*\}', update_advertising_board, content)

# 3. Add prominent INETRA Billboards at key city locations (Junction 25, 26, 27)
extra_billboards = """
# ==============================================================================
# INETRA SMART CITY SENSING PLATFORM BILLBOARDS
# ==============================================================================
AdvertisingBoard {
  translation -65.0 65.0 0
  rotation 0 0 1 0.785398
  frontTexture [ "textures/custom_signboard_logo.png" ]
  backTexture [ "textures/custom_signboard_logo.png" ]
  displayBackLight TRUE
  displayWidth 10
  displayHeight 8
  frameThickness 0.8
  frameColor 0.1 0.3 0.6
  poleNumber 2
  poleHeight 9
  baseRatio 5.8
}

AdvertisingBoard {
  translation 65.0 -65.0 0
  rotation 0 0 1 -2.35619
  frontTexture [ "textures/custom_signboard_logo.png" ]
  backTexture [ "textures/custom_signboard_logo.png" ]
  displayBackLight TRUE
  displayWidth 10
  displayHeight 8
  frameThickness 0.8
  frameColor 0.1 0.3 0.6
  poleNumber 2
  poleHeight 9
  baseRatio 5.8
}

AdvertisingBoard {
  translation 125.0 115.0 0
  rotation 0 0 1 2.35619
  frontTexture [ "textures/custom_signboard_logo.png" ]
  backTexture [ "textures/custom_signboard_logo.png" ]
  displayBackLight TRUE
  displayWidth 10
  displayHeight 8
  frameThickness 0.8
  frameColor 0.1 0.3 0.6
  poleNumber 2
  poleHeight 9
  baseRatio 5.8
}
"""

# Append billboards before traffic light nodes
idx = content.find("# ==============================================================================\n# SLEEK 4-WAY INDIAN TRAFFIC LIGHT POST")
if idx == -1:
    idx = content.find("# ==============================================================================\n# UNBLOCKED 5-ASPECT")
if idx == -1:
    idx = content.find("# ==============================================================================")

if idx != -1:
    new_wbt = content[:idx] + extra_billboards + "\n\n" + content[idx:]
else:
    new_wbt = content + "\n\n" + extra_billboards

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(new_wbt)

print(f"Successfully replaced all signboards and billboards with the INETRA platform logo in {WBT_PATH}")
