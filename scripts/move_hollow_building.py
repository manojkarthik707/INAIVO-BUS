import re

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"

with open(WBT_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace HollowBuilding definition
content = re.sub(
    r'HollowBuilding\s*\{[^}]*\}',
    'HollowBuilding {\n  translation -68.0 82.0 0\n  rotation 0 0 1 1.5708\n}',
    content
)

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Moved HollowBuilding to translation -68.0 82.0 0 near UBuilding in {WBT_PATH}")
