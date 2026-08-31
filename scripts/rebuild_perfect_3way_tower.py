import re

def generate_perfect_3way_post():
    # 1. South Face: Standard 3-Aspect (Red, Amber, Green) facing South (shines -Y towards Northbound drivers)
    south_face = """
        Transform {
          translation 0.0 0.45 3.4
          rotation 0 0 1 0.0
          children [
            Shape {
              appearance PBRAppearance { baseColor 0.08 0.08 0.09 roughness 0.4 metalness 0.8 }
              geometry Box { size 0.38 0.22 0.95 }
            }
            Transform {
              translation 0 0.115 0
              children [
                Shape {
                  appearance PBRAppearance { baseColor 0.95 0.75 0.05 roughness 0.2 metalness 0.1 }
                  geometry Box { size 0.44 0.015 1.02 }
                }
              ]
            }
            # Red
            Transform {
              translation 0 0.125 0.28
              rotation 1 0 0 1.5708
              children [
                Shape {
                  appearance DEF MAT_41_SOUTH_RED PBRAppearance {
                    baseColor 0.2 0.02 0.02 emissiveColor 1.0 0.05 0.05 roughness 0.1 metalness 0.0
                  }
                  geometry Cylinder { height 0.015 radius 0.11 }
                }
              ]
            }
            # Amber
            Transform {
              translation 0 0.125 0.02
              rotation 1 0 0 1.5708
              children [
                Shape {
                  appearance DEF MAT_41_SOUTH_AMBER PBRAppearance {
                    baseColor 0.2 0.18 0.02 emissiveColor 0.0 0.0 0.0 roughness 0.1 metalness 0.0
                  }
                  geometry Cylinder { height 0.015 radius 0.11 }
                }
              ]
            }
            # Straight Green
            Transform {
              translation 0 0.125 -0.24
              rotation 1 0 0 1.5708
              children [
                Shape {
                  appearance DEF MAT_41_SOUTH_STRAIGHT PBRAppearance {
                    baseColor 0.02 0.2 0.05 emissiveColor 0.0 0.0 0.0 roughness 0.1 metalness 0.0
                  }
                  geometry Cylinder { height 0.015 radius 0.11 }
                }
              ]
            }
          ]
        }
    """

    # 2. North Face: Standard 3-Aspect (Red, Amber, Green) facing North (shines +Y towards Southbound drivers)
    north_face = """
        Transform {
          translation 0.0 -0.45 3.4
          rotation 0 0 1 3.1415926
          children [
            Shape {
              appearance PBRAppearance { baseColor 0.08 0.08 0.09 roughness 0.4 metalness 0.8 }
              geometry Box { size 0.38 0.22 0.95 }
            }
            Transform {
              translation 0 0.115 0
              children [
                Shape {
                  appearance PBRAppearance { baseColor 0.95 0.75 0.05 roughness 0.2 metalness 0.1 }
                  geometry Box { size 0.44 0.015 1.02 }
                }
              ]
            }
            # Red
            Transform {
              translation 0 0.125 0.28
              rotation 1 0 0 1.5708
              children [
                Shape {
                  appearance DEF MAT_41_NORTH_RED PBRAppearance {
                    baseColor 0.2 0.02 0.02 emissiveColor 1.0 0.05 0.05 roughness 0.1 metalness 0.0
                  }
                  geometry Cylinder { height 0.015 radius 0.11 }
                }
              ]
            }
            # Amber
            Transform {
              translation 0 0.125 0.02
              rotation 1 0 0 1.5708
              children [
                Shape {
                  appearance DEF MAT_41_NORTH_AMBER PBRAppearance {
                    baseColor 0.2 0.18 0.02 emissiveColor 0.0 0.0 0.0 roughness 0.1 metalness 0.0
                  }
                  geometry Cylinder { height 0.015 radius 0.11 }
                }
              ]
            }
            # Straight Green
            Transform {
              translation 0 0.125 -0.24
              rotation 1 0 0 1.5708
              children [
                Shape {
                  appearance DEF MAT_41_NORTH_STRAIGHT PBRAppearance {
                    baseColor 0.02 0.2 0.05 emissiveColor 0.0 0.0 0.0 roughness 0.1 metalness 0.0
                  }
                  geometry Cylinder { height 0.015 radius 0.11 }
                }
              ]
            }
          ]
        }
    """

    # 3. East Face: Facing EAST (rot -1.5707963, shines +X towards Westbound Shortcut drivers)
    # With Red, Amber, Green, Free-Left Arrow (Left) and Right Turn Arrow (Right)
    east_face = """
        Transform {
          translation -0.45 0.0 3.4
          rotation 0 0 1 -1.5707963
          children [
            Shape {
              appearance PBRAppearance { baseColor 0.08 0.08 0.09 roughness 0.4 metalness 0.8 }
              geometry Box { size 0.38 0.22 1.25 }
            }
            Transform {
              translation 0 0.115 0
              children [
                Shape {
                  appearance PBRAppearance { baseColor 0.95 0.75 0.05 roughness 0.2 metalness 0.1 }
                  geometry Box { size 0.44 0.015 1.32 }
                }
              ]
            }
            # Red
            Transform {
              translation 0 0.125 0.38
              rotation 1 0 0 1.5708
              children [
                Shape {
                  appearance DEF MAT_41_EAST_RED PBRAppearance {
                    baseColor 0.2 0.02 0.02 emissiveColor 1.0 0.05 0.05 roughness 0.1 metalness 0.0
                  }
                  geometry Cylinder { height 0.015 radius 0.11 }
                }
              ]
            }
            # Amber
            Transform {
              translation 0 0.125 0.12
              rotation 1 0 0 1.5708
              children [
                Shape {
                  appearance DEF MAT_41_EAST_AMBER PBRAppearance {
                    baseColor 0.2 0.18 0.02 emissiveColor 0.0 0.0 0.0 roughness 0.1 metalness 0.0
                  }
                  geometry Cylinder { height 0.015 radius 0.11 }
                }
              ]
            }
            # Green
            Transform {
              translation 0 0.125 -0.14
              rotation 1 0 0 1.5708
              children [
                Shape {
                  appearance DEF MAT_41_EAST_STRAIGHT PBRAppearance {
                    baseColor 0.02 0.2 0.05 emissiveColor 0.0 0.0 0.0 roughness 0.1 metalness 0.0
                  }
                  geometry Cylinder { height 0.015 radius 0.11 }
                }
              ]
            }
            # Free-Left Arrow (Left side from driver perspective: X = +0.14)
            Transform {
              translation 0.14 0.125 -0.38
              rotation 1 0 0 1.5708
              children [
                Shape {
                  appearance DEF MAT_41_EAST_LEFT PBRAppearance {
                    baseColor 0.02 0.2 0.05 emissiveColor 0.05 1.0 0.2 roughness 0.1 metalness 0.0
                  }
                  geometry Cylinder { height 0.015 radius 0.075 }
                }
              ]
            }
            # Right Turn Arrow (Right side from driver perspective: X = -0.14)
            Transform {
              translation -0.14 0.125 -0.38
              rotation 1 0 0 1.5708
              children [
                Shape {
                  appearance DEF MAT_41_EAST_RIGHT PBRAppearance {
                    baseColor 0.02 0.2 0.05 emissiveColor 0.0 0.0 0.0 roughness 0.1 metalness 0.0
                  }
                  geometry Cylinder { height 0.015 radius 0.075 }
                }
              ]
            }
          ]
        }
    """

    return f"""
# ==============================================================================
# PERFECT 3-WAY INDIAN TRAFFIC LIGHT MERGING POST: TRAFFIC_LIGHT_JUNCTION_41
# ==============================================================================
DEF TRAFFIC_LIGHT_JUNCTION_41 Robot {{
  translation -45.0 4.5 0.0
  rotation 0 0 1 0.0
  children [
    # 1. Concrete Base Island
    Transform {{
      translation 0 0 0.12
      children [
        Shape {{
          appearance PBRAppearance {{ baseColor 0.15 0.15 0.16 roughness 0.8 metalness 0.1 }}
          geometry Cylinder {{ height 0.24 radius 1.1 }}
        }}
      ]
    }}
    # Yellow Reflective Ring
    Transform {{
      translation 0 0 0.14
      children [
        Shape {{
          appearance PBRAppearance {{ baseColor 0.95 0.75 0.05 roughness 0.3 metalness 0.1 }}
          geometry Cylinder {{ height 0.26 radius 1.12 }}
        }}
      ]
    }}
    # 2. Sleek Center Mast
    Transform {{
      translation 0 0 2.2
      children [
        Shape {{
          appearance PBRAppearance {{ baseColor 0.08 0.08 0.09 roughness 0.3 metalness 0.9 }}
          geometry Cylinder {{ height 4.2 radius 0.09 }}
        }}
      ]
    }}
    # 3. 3-Way Heads
    {south_face}
    {north_face}
    {east_face}
  ]
  name "traffic_light_junction_41"
  controller "traffic_light_controller"
  supervisor TRUE
  locked TRUE
}}
"""

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"
with open(WBT_PATH, 'r', encoding='utf-8') as f:
    wbt = f.read()

# Clean old post and append perfect 3-way post
wbt = re.sub(r'# ==============================================================================\n# (?:SLEEK|TAILORED|PERFECT) 3-WAY INDIAN TRAFFIC LIGHT MERGING POST:[^#]*', '', wbt)
wbt = re.sub(r'DEF TRAFFIC_LIGHT_JUNCTION_41 Robot \{[^}]*(?:\{[^}]*\}[^}]*)*\}', '', wbt)

# Find clean end of junction 27
idx_j27 = wbt.find('name "traffic_light_junction_27"')
if idx_j27 != -1:
    idx_end = wbt.find('locked TRUE\n}', idx_j27)
    if idx_end != -1:
        base_wbt = wbt[:idx_end + len('locked TRUE\n}')]
    else:
        base_wbt = wbt
else:
    base_wbt = wbt

new_post = generate_perfect_3way_post()
final_wbt = base_wbt.rstrip() + "\n\n" + new_post.strip() + "\n"

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(final_wbt)

print(f"Correctly oriented East-facing merging traffic light island in {WBT_PATH}")
