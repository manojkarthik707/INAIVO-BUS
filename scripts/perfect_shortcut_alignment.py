import re

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"
with open(WBT_PATH, 'r', encoding='utf-8') as f:
    wbt = f.read()

# 1. Exact Webots StraightRoadSegment for road_central_shortcut:
# Start point: translation -45.0 -4.5 0.02 (Junction 41)
# Rotation: 0 0 1 0.09966865 (5.71 degrees towards Junction 43 at +45, +4.5)
# Length: 90.45m
# Width: 10.75m (2-lane road: 1 forward, 1 reverse)
road_wbt = """StraightRoadSegment {
  translation -45 -4.5 0.02
  rotation 0 0 1 0.09966865
  name "road_central_shortcut"
  width 10.75
  numberOfLanes 2
  numberOfForwardLanes 1
  lines [
    RoadLine {
      color 0.85 0.75 0.3
      type "dashed"
      width 0.15
    }
  ]
  startJunction "41"
  endJunction "43"
  rightBorder FALSE
  leftBorder FALSE
  length 90.45
}"""

# Replace road_central_shortcut
wbt = re.sub(
    r'(DEF\s+\w+\s+)?StraightRoadSegment\s*\{[^}]*name\s+"road_central_shortcut"[^}]*\}',
    road_wbt,
    wbt
)

# Also handle if name "road_central_shortcut" comes right after opening brace
wbt = re.sub(
    r'StraightRoadSegment\s*\{[^}]*name\s+"road_central_shortcut"[^}]*lines\s*\[[^\]]*\][^}]*\}',
    road_wbt,
    wbt
)

# 2. Set exact Traffic Light post positions:
# Junction 41 Island at (-45.0, -4.5, 0.0)
wbt = re.sub(r'DEF\s+TRAFFIC_LIGHT_JUNCTION_41\s+Robot\s*\{\s*translation\s+[-0-9.]+\s+[-0-9.]+\s+[-0-9.]+',
             'DEF TRAFFIC_LIGHT_JUNCTION_41 Robot {\n  translation -45.0 -4.5 0.0', wbt)

# Junction 43 Island at (45.0, 4.5, 0.0)
wbt = re.sub(r'DEF\s+TRAFFIC_LIGHT_JUNCTION_43\s+Robot\s*\{\s*translation\s+[-0-9.]+\s+[-0-9.]+\s+[-0-9.]+',
             'DEF TRAFFIC_LIGHT_JUNCTION_43 Robot {\n  translation 45.0 4.5 0.0', wbt)

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(wbt)

print(f"Perfected shortcut road geometry in {WBT_PATH}:")
print("  Start (Junction 41): (-45.0, -4.5)")
print("  End (Junction 43):   (+45.0, +4.5)")
print("  Length: 90.45m, Width: 10.75m (2 lanes)")
print("  TL 41: (-45.0, -4.5), TL 43: (45.0, 4.5)")
