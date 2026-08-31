import re

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"

with open(WBT_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Update HollowBuilding position to (-130.0, 82.0, 0) with a clean rotation
content = re.sub(
    r'HollowBuilding\s*\{[^}]*\}',
    'HollowBuilding {\n  translation -130.0 82.0 0\n  rotation 0 0 1 0.785398\n}',
    content
)

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Relocated HollowBuilding to translation -130.0 82.0 0 (43m clear from UBuilding) in {WBT_PATH}")
