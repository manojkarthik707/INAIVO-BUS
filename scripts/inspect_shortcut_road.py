with open(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt", 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'StraightRoadSegment\s*\{[^}]*road_central_shortcut[^}]*\}', text)
if m:
    print("Found road_central_shortcut:")
    print(m.group(0))
else:
    print("road_central_shortcut not found directly, searching all road segments:")
    for m in re.finditer(r'(StraightRoadSegment|CurvedRoadSegment)\s*\{([^}]+)\}', text):
        block = m.group(0)
        if '-25' in block or 'shortcut' in block:
            print(block[:300])
