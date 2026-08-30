import re

path = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

new_routes = """
# ── OFF-ROAD DIRT & GRAVEL TRAILS ───────────────────────────────────────
StraightRoadSegment {
  translation -64.5 -105 0.025
  rotation 0 0 1 -0.5236
  name "offroad_south_trail_1"
  width 8.0
  numberOfLanes 2
  numberOfForwardLanes 1
  appearance PBRAppearance {
    baseColor 0.52 0.42 0.32
    roughness 0.95
    metalness 0
  }
  lines [
    RoadLine {
      color 0.6 0.5 0.4
      type "dashed"
    }
  ]
  rightBorder FALSE
  leftBorder FALSE
  length 80
}

StraightRoadSegment {
  translation 5.0 -145 0.025
  rotation 0 0 1 -0.54
  name "offroad_south_trail_2"
  width 8.0
  numberOfLanes 2
  numberOfForwardLanes 1
  appearance PBRAppearance {
    baseColor 0.52 0.42 0.32
    roughness 0.95
    metalness 0
  }
  lines [
    RoadLine {
      color 0.6 0.5 0.4
      type "dashed"
    }
  ]
  rightBorder FALSE
  leftBorder FALSE
  length 84
}

# ── NARROW URBAN ALLEYWAYS & MIDTOWN SHORTCUTS ──────────────────────────
StraightRoadSegment {
  translation -4.5 4.5 0.02
  rotation 0 0 1 -1.5708
  name "midtown_central_alley"
  width 10.75
  numberOfLanes 2
  numberOfForwardLanes 1
  lines [
    RoadLine {
      color 0.85 0.75 0.3
      type "dashed"
    }
  ]
  rightBorder FALSE
  leftBorder FALSE
  length 49.5
}

StraightRoadSegment {
  translation 45.0 4.5 0.02
  name "east_commercial_cross_shortcut"
  width 10.75
  numberOfLanes 2
  numberOfForwardLanes 1
  lines [
    RoadLine {
      color 0.85 0.75 0.3
      type "dashed"
    }
  ]
  rightBorder FALSE
  leftBorder FALSE
  length 60
}

# ── NORTH-WEST SCENIC 2-LANE BYPASS ────────────────────────────────────
StraightRoadSegment {
  translation -105.0 4.5 0.02
  rotation 0 0 1 1.5708
  name "west_side_bypass_street"
  width 10.75
  numberOfLanes 2
  numberOfForwardLanes 1
  lines [
    RoadLine {
      color 0.85 0.75 0.3
      type "dashed"
    }
  ]
  rightBorder FALSE
  leftBorder FALSE
  length 60
}
"""

if "offroad_south_trail_1" not in content:
    target = "DEF PEDESTRIAN_01 Pedestrian"
    content = content.replace(target, new_routes + "\n" + target)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully added off-road dirt trails, narrow urban alleys, and shortcuts to the city map!")
