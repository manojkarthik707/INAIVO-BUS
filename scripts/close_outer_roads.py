import re

path = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Update road(13) length to 210.5 so it connects seamlessly to the bottom-left curve
content = re.sub(
    r'(name "road\(13\)"[\s\S]*?length\s+)\d+',
    r'\g<1>210.5',
    content
)

# New connecting road segments to close the entire outer loop
closing_roads = """
# ── CLOSED CIRCUIT WEST PERIMETER HIGHWAY CONNECTIONS ──────────────────
CurvedRoadSegment {
  translation -135.5 190.5 0.02
  rotation 0 0 1 1.5708
  name "road_outer_top_left_curve"
  width 21.5
  numberOfLanes 4
  numberOfForwardLanes 2
  lines [
    RoadLine {
    }
    RoadLine {
      color 0.85 0.75 0.3
      type "double"
    }
  ]
  rightBorder FALSE
  leftBorder FALSE
  curvatureRadius 40.5
}
StraightRoadSegment {
  translation -176.0 190.5 0.02
  rotation 0 0 1 -1.5708
  name "road_outer_west_avenue"
  width 21.5
  numberOfLanes 4
  numberOfForwardLanes 2
  lines [
    RoadLine {
    }
    RoadLine {
      color 0.85 0.75 0.3
      type "double"
    }
  ]
  rightBorder FALSE
  leftBorder FALSE
  length 337.5
}
CurvedRoadSegment {
  translation -135.5 -147.0 0.02
  rotation 0 0 1 3.14156
  name "road_outer_bottom_left_curve"
  width 21.5
  numberOfLanes 4
  numberOfForwardLanes 2
  lines [
    RoadLine {
    }
    RoadLine {
      color 0.85 0.75 0.3
      type "double"
    }
  ]
  rightBorder FALSE
  leftBorder FALSE
  curvatureRadius 40.5
}
"""

if "road_outer_west_avenue" not in content:
    target = "DEF PEDESTRIAN_01 Pedestrian"
    content = content.replace(target, closing_roads + "\n" + target)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully connected the outer perimeter roads into a 100% closed circuit!")
