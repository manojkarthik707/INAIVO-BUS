import re

def generate_sleek_3way_vrml(def_name, j_id, tx, ty):
    # Generates a 3-way Indian Traffic Light Island with signal heads facing South, North, and East:
    # 0 deg: Face South
    # 180 deg: Face North
    # 90 deg: Face East (Shortcut Merging Approach)
    faces = [
        ("south", 0.0, 0.45, 0.0),
        ("north", 0.0, -0.45, 3.1415926),
        ("east", 0.45, 0.0, 1.5707963),
    ]

    face_vrml_list = []
    for face_name, ox, oy, rot_z in faces:
        face_vrml_list.append(f"""
        Transform {{
          translation {ox:.2f} {oy:.2f} 3.4
          rotation 0 0 1 {rot_z}
          children [
            # Main Signal Housing Box
            Shape {{
              appearance PBRAppearance {{
                baseColor 0.08 0.08 0.09
                roughness 0.4
                metalness 0.8
              }}
              geometry Box {{
                size 0.38 0.22 1.25
              }}
            }}
            # Yellow Border Frame
            Transform {{
              translation 0 0.115 0
              children [
                Shape {{
                  appearance PBRAppearance {{
                    baseColor 0.95 0.75 0.05
                    roughness 0.2
                    metalness 0.1
                  }}
                  geometry Box {{
                    size 0.44 0.015 1.32
                  }}
                }}
              ]
            }}
            # 1. Red Lens
            Transform {{
              translation 0 0.125 0.38
              rotation 1 0 0 1.5708
              children [
                DEF TLS_{j_id}_{face_name.upper()}_RED Shape {{
                  appearance PBRAppearance {{
                    baseColor 0.2 0.02 0.02
                    emissiveColor 1.0 0.05 0.05
                    roughness 0.1
                    metalness 0.0
                  }}
                  geometry Cylinder {{
                    height 0.015
                    radius 0.11
                  }}
                }}
              ]
            }}
            # 2. Yellow Lens
            Transform {{
              translation 0 0.125 0.12
              rotation 1 0 0 1.5708
              children [
                DEF TLS_{j_id}_{face_name.upper()}_YELLOW Shape {{
                  appearance PBRAppearance {{
                    baseColor 0.2 0.18 0.02
                    emissiveColor 0.0 0.0 0.0
                    roughness 0.1
                    metalness 0.0
                  }}
                  geometry Cylinder {{
                    height 0.015
                    radius 0.11
                  }}
                }}
              ]
            }}
            # 3. Green Straight Lens
            Transform {{
              translation 0 0.125 -0.14
              rotation 1 0 0 1.5708
              children [
                DEF TLS_{j_id}_{face_name.upper()}_GREEN Shape {{
                  appearance PBRAppearance {{
                    baseColor 0.02 0.2 0.05
                    emissiveColor 0.0 0.0 0.0
                    roughness 0.1
                    metalness 0.0
                  }}
                  geometry Cylinder {{
                    height 0.015
                    radius 0.11
                  }}
                }}
              ]
            }}
            # 4. Green Free-Left Arrow (Left side from driver perspective: X = +0.18)
            Transform {{
              translation 0.18 0.125 -0.38
              rotation 1 0 0 1.5708
              children [
                DEF TLS_{j_id}_{face_name.upper()}_LEFT Shape {{
                  appearance PBRAppearance {{
                    baseColor 0.02 0.2 0.05
                    emissiveColor 0.05 1.0 0.2
                    roughness 0.1
                    metalness 0.0
                  }}
                  geometry Cylinder {{
                    height 0.015
                    radius 0.075
                  }}
                }}
              ]
            }}
            # 5. Protected Right Arrow (Right side from driver perspective: X = -0.18)
            Transform {{
              translation -0.18 0.125 -0.38
              rotation 1 0 0 1.5708
              children [
                DEF TLS_{j_id}_{face_name.upper()}_RIGHT Shape {{
                  appearance PBRAppearance {{
                    baseColor 0.02 0.2 0.05
                    emissiveColor 0.0 0.0 0.0
                    roughness 0.1
                    metalness 0.0
                  }}
                  geometry Cylinder {{
                    height 0.015
                    radius 0.075
                  }}
                }}
              ]
            }}
          ]
        }}
        """)

    faces_combined = "".join(face_vrml_list)

    return f"""
# ==============================================================================
# SLEEK 3-WAY INDIAN TRAFFIC LIGHT MERGING POST: {def_name}
# ==============================================================================
DEF {def_name} Robot {{
  translation {tx:.2f} {ty:.2f} 0.0
  rotation 0 0 1 0.0
  children [
    # 1. Concrete Island Base
    Transform {{
      translation 0 0 0.12
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.15 0.15 0.16
            roughness 0.8
            metalness 0.1
          }}
          geometry Cylinder {{
            height 0.24
            radius 1.1
          }}
        }}
      ]
    }}
    # Yellow Reflective Base Ring
    Transform {{
      translation 0 0 0.14
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.95 0.75 0.05
            roughness 0.3
            metalness 0.1
          }}
          geometry Cylinder {{
            height 0.26
            radius 1.12
          }}
        }}
      ]
    }}
    # 2. Sleek Central Steel Mast
    Transform {{
      translation 0 0 2.2
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.08 0.08 0.09
            roughness 0.3
            metalness 0.9
          }}
          geometry Cylinder {{
            height 4.2
            radius 0.09
          }}
        }}
      ]
    }}
    # 3. 3-Way Signal Heads (South, North, East)
    {faces_combined}
  ]
  name "traffic_light_junction_{j_id}"
  controller "traffic_light_controller"
  supervisor TRUE
  locked TRUE
}}
"""

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"

with open(WBT_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Complete the shortcut road to connect seamlessly from X=-45.0 to X=+45.0 (length 90.0)
content = re.sub(
    r'StraightRoadSegment\s*\{[^}]*name\s*"road_central_shortcut"[^}]*\}',
    """StraightRoadSegment {
  translation -45.0 4.5 0.02
  name "road_central_shortcut"
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
  length 90.0
}""",
    content
)

# 2. Remove any previous junction 41 traffic light post
content = re.sub(r'# ==============================================================================\n# SLEEK 3-WAY INDIAN TRAFFIC LIGHT MERGING POST:[^#]*', '', content)

# 3. Generate the new 3-way traffic light post at (-45.0, 4.5)
tls_3way = generate_sleek_3way_vrml("TRAFFIC_LIGHT_JUNCTION_41", "41", -45.0, 4.5)

# Append at the end of the world
content = content.rstrip() + "\n\n" + tls_3way + "\n"

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Completed shortcut road (length 90.0) and installed 3-way traffic light at merging area (-45.0, 4.5) in {WBT_PATH}")
