import re

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"

with open(WBT_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove all old AdvertisingBoard nodes
content = re.sub(r'AdvertisingBoard\s*\{[^}]*\}', '', content)

# 2. Add perfectly positioned, non-overexposed (displayBackLight FALSE) square INETRA Billboards
# in open roadside plazas with ZERO building clipping:
clean_billboards = """
# ==============================================================================
# INETRA SMART CITY SENSING PLATFORM BILLBOARDS (1:1 Aspect Ratio, Zero Clipping)
# ==============================================================================
AdvertisingBoard {
  name "inetra_billboard_j26_plaza"
  translation -30.0 60.0 0
  rotation 0 0 1 2.35619
  frontTexture [ "textures/custom_signboard_logo.png" ]
  backTexture [ "textures/custom_signboard_logo.png" ]
  displayBackLight FALSE
  displayWidth 7.0
  displayHeight 7.0
  frameThickness 0.4
  frameColor 0.08 0.18 0.35
  poleNumber 2
  poleHeight 6.5
  baseRatio 5.8
}

AdvertisingBoard {
  name "inetra_billboard_j25_plaza"
  translation 30.0 -30.0 0
  rotation 0 0 1 -0.785398
  frontTexture [ "textures/custom_signboard_logo.png" ]
  backTexture [ "textures/custom_signboard_logo.png" ]
  displayBackLight FALSE
  displayWidth 7.0
  displayHeight 7.0
  frameThickness 0.4
  frameColor 0.08 0.18 0.35
  poleNumber 2
  poleHeight 6.5
  baseRatio 5.8
}

AdvertisingBoard {
  name "inetra_billboard_j27_plaza"
  translation 120.0 80.0 0
  rotation 0 0 1 0.785398
  frontTexture [ "textures/custom_signboard_logo.png" ]
  backTexture [ "textures/custom_signboard_logo.png" ]
  displayBackLight FALSE
  displayWidth 7.0
  displayHeight 7.0
  frameThickness 0.4
  frameColor 0.08 0.18 0.35
  poleNumber 2
  poleHeight 6.5
  baseRatio 5.8
}
"""

# Insert before traffic lights
idx = content.find("# ==============================================================================\n# SLEEK 4-WAY INDIAN TRAFFIC LIGHT POST")
if idx == -1:
    idx = content.find("# ==============================================================================\n# UNBLOCKED 5-ASPECT")
if idx == -1:
    idx = content.find("# ==============================================================================")

if idx != -1:
    new_wbt = content[:idx] + clean_billboards + "\n\n" + content[idx:]
else:
    new_wbt = content + "\n\n" + clean_billboards

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(new_wbt)

print(f"Cleanly positioned billboards with displayBackLight FALSE and 1:1 aspect ratio in {WBT_PATH}")
