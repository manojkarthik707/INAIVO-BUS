import re

with open(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt", 'r', encoding='utf-8') as f:
    text = f.read()

# Find all building translations
for m in re.finditer(r'(CommercialBuilding|BuildingUnderConstruction|UBuilding|HollowBuilding|Hotel|TheThreeTowers|CyberboticsTower|BigGlassTower|Auditorium|Museum|ResidentialBuilding|FastFoodRestaurant|SimpleBuilding)\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}', text):
    block = m.group(0)
    name_m = re.search(r'name\s*"([^"]+)"', block)
    trans_m = re.search(r'translation\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)', block)
    if trans_m:
        print(f"Building: {name_m.group(1) if name_m else 'unnamed'} at ({trans_m.group(1)}, {trans_m.group(2)})")
