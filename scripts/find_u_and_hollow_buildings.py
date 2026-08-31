import re

with open(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt", 'r', encoding='utf-8') as f:
    text = f.read()

for proto in ['UBuilding', 'HollowBuilding', 'CommercialBuilding', 'Hotel', 'BuildingUnderConstruction']:
    m = re.search(r'(' + proto + r'\s*\{[^}]+\})', text)
    if m:
        print(f"=== {proto} ===")
        print(m.group(1))
