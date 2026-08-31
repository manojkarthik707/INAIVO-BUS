import re
import math

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"
with open(WBT_PATH, 'r', encoding='utf-8') as f:
    wbt = f.read()

# 1. Align road_central_shortcut with SUMO coordinates:
# SUMO 41: (-45.0, -4.5)
# SUMO 43: (+45.0, +4.5)
# Midpoint: (0.0, 0.0)
# Angle: atan2(9.0, 90.0) = 0.09966865 rad
# Length: sqrt(90^2 + 9^2) = 90.4488m

# Locate road_central_shortcut
old_road = re.search(r'DEF\s+road_central_shortcut\s+StraightRoadSegment\s*\{[^}]*\}', wbt)
new_road = """DEF road_central_shortcut StraightRoadSegment {
  translation 0 0 0
  rotation 0 0 1 0.09966865
  name "road_central_shortcut"
  width 10.76
  numberOfLanes 2
  numberOfForwardLanes 1
  lines [
    RoadLine {
      color 0.85 0.75 0.1
      type "dashed"
      width 0.15
    }
  ]
  startJunction "none"
  endJunction "none"
  length 90.45
  locked TRUE
}"""

if old_road:
    wbt = wbt[:old_road.start()] + new_road + wbt[old_road.end():]
    print("Replaced road_central_shortcut with exact angled alignment matching SUMO coordinates.")

# 2. Re-position TRAFFIC_LIGHT_JUNCTION_41 to (-45.0, -4.5)
# Move island off the active driving path:
# At Junction 41 (-45.0, -4.5): placed on the corner curb at (-45.0, -9.5) or (-45.0, -4.5) with appropriate scale
wbt = re.sub(r'DEF\s+TRAFFIC_LIGHT_JUNCTION_41\s+Robot\s*\{\s*translation\s+[-0-9.]+\s+[-0-9.]+\s+[-0-9.]+', 
             'DEF TRAFFIC_LIGHT_JUNCTION_41 Robot {\n  translation -45.0 -4.5 0.0', wbt)

# 3. Re-position TRAFFIC_LIGHT_JUNCTION_43 to (+45.0, +4.5)
wbt = re.sub(r'DEF\s+TRAFFIC_LIGHT_JUNCTION_43\s+Robot\s*\{\s*translation\s+[-0-9.]+\s+[-0-9.]+\s+[-0-9.]+', 
             'DEF TRAFFIC_LIGHT_JUNCTION_43 Robot {\n  translation 45.0 4.5 0.0', wbt)

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(wbt)

print(f"Updated road and signal island positions in {WBT_PATH}")
