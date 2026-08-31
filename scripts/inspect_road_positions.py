with open(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt", 'r', encoding='utf-8') as f:
    wbt = f.read()

import re

# Find road_central_shortcut
m = re.search(r'DEF\s+road_central_shortcut\s+StraightRoadSegment\s*\{[^}]*\}', wbt)
if m:
    print("=== road_central_shortcut ===")
    print(m.group(0))

# Find TRAFFIC_LIGHT_JUNCTION_41 and 43
m41 = re.search(r'DEF\s+TRAFFIC_LIGHT_JUNCTION_41\s+Robot\s*\{[^\n]*\ntranslation\s+([^\n]+)', wbt)
m43 = re.search(r'DEF\s+TRAFFIC_LIGHT_JUNCTION_43\s+Robot\s*\{[^\n]*\ntranslation\s+([^\n]+)', wbt)
print(f"TL 41 translation: {m41.group(1) if m41 else 'not found'}")
print(f"TL 43 translation: {m43.group(1) if m43 else 'not found'}")

# Find nearby straight roads
for rname in ['road_23', 'road_24', 'road_5', 'road_6', 'road_7', 'road_8', 'road_9']:
    m_r = re.search(rf'DEF\s+{rname}\s+StraightRoadSegment\s*\{{[^}}]*\}}', wbt)
    if m_r:
        print(f"=== {rname} ===")
        print(m_r.group(0))
