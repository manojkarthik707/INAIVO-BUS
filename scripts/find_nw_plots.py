import re
import math

with open(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt", 'r', encoding='utf-8') as f:
    text = f.read()

# Check roads and buildings in northwest quadrant (X < 0, Y > 0)
print("=== ROAD SEGMENTS IN NW QUADRANT ===")
for m in re.finditer(r'(CurvedRoadSegment|StraightRoadSegment)\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}', text):
    block = m.group(0)
    tm = re.search(r'translation\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)', block)
    name_m = re.search(r'name\s*"([^"]+)"', block)
    if tm:
        x, y = float(tm.group(1)), float(tm.group(2))
        if x < 0 and y > 0:
            print(f"Road {name_m.group(1) if name_m else 'road'} at ({x:.2f}, {y:.2f})")

print("\n=== BUILDINGS IN NW QUADRANT ===")
for m in re.finditer(r'(CommercialBuilding|BuildingUnderConstruction|UBuilding|HollowBuilding|Hotel|TheThreeTowers|CyberboticsTower|BigGlassTower|Auditorium|Museum|ResidentialBuilding|FastFoodRestaurant|SimpleBuilding)\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}', text):
    block = m.group(0)
    tm = re.search(r'translation\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)', block)
    name_m = re.search(r'name\s*"([^"]+)"', block)
    if tm:
        x, y = float(tm.group(1)), float(tm.group(2))
        if x < 0 and y > 0:
            print(f"Building {name_m.group(1) if name_m else m.group(1)} at ({x:.2f}, {y:.2f})")
