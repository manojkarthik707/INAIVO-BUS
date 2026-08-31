import re

def generate_clean_t_junction_post():
    # North Head: Southbound traffic on Road 23 (rot 0 0 1 0.0)
    # Red, Amber, Straight Green + LEFT Turn Arrow (turning East into shortcut)
    north_head = """
    Pose {
      translation 0.0 0.45 3.4
      rotation 0 0 1 0.0
      children [
        Shape {
          appearance PBRAppearance { baseColor 0.08 0.08 0.09 roughness 0.4 metalness 0.8 }
          geometry Box { size 0.54 0.22 1.25 }
        }
        Pose {
          translation 0 0.115 0
          children [
            Shape {
              appearance PBRAppearance { baseColor 0.95 0.75 0.05 roughness 0.2 metalness 0.1 }
              geometry Box { size 0.60 0.015 1.32 }
            }
          ]
        }
        # Red
        Pose {
          translation -0.05 0.125 0.38
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
        Pose {
          translation -0.05 0.125 0.12
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
        Pose {
          translation -0.05 0.125 -0.14
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
        # Left Turn Arrow (Turning East into Shortcut: Driver's Left = +0.16)
        Pose {
          translation 0.16 0.125 -0.14
          rotation 1 0 0 1.5708
          children [
            Shape {
              appearance DEF MAT_41_NORTH_LEFT PBRAppearance {
                baseColor 0.02 0.2 0.05 emissiveColor 0.05 1.0 0.2 roughness 0.1 metalness 0.0
              }
              geometry Cylinder { height 0.015 radius 0.095 }
            }
          ]
        }
      ]
    }
    """

    # South Head: Northbound traffic on Road 23 (rot 0 0 1 3.1415926)
    # Red, Amber, Straight Green + RIGHT Turn Arrow (turning East into shortcut)
    south_head = """
    Pose {
      translation 0.0 -0.45 3.4
      rotation 0 0 1 3.1415926
      children [
        Shape {
          appearance PBRAppearance { baseColor 0.08 0.08 0.09 roughness 0.4 metalness 0.8 }
          geometry Box { size 0.54 0.22 1.25 }
        }
        Pose {
          translation 0 0.115 0
          children [
            Shape {
              appearance PBRAppearance { baseColor 0.95 0.75 0.05 roughness 0.2 metalness 0.1 }
              geometry Box { size 0.60 0.015 1.32 }
            }
          ]
        }
        # Red
        Pose {
          translation 0.05 0.125 0.38
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
        Pose {
          translation 0.05 0.125 0.12
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
        Pose {
          translation 0.05 0.125 -0.14
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
        # Right Turn Arrow (Turning East into Shortcut: Driver's Right = -0.16)
        Pose {
          translation -0.16 0.125 -0.14
          rotation 1 0 0 1.5708
          children [
            Shape {
              appearance DEF MAT_41_SOUTH_RIGHT PBRAppearance {
                baseColor 0.02 0.2 0.05 emissiveColor 0.0 0.0 0.0 roughness 0.1 metalness 0.0
              }
              geometry Cylinder { height 0.015 radius 0.095 }
            }
          ]
        }
      ]
    }
    """

    # East Head: Merging Shortcut Approach (rot 0 0 1 -1.5707963)
    # Exactly TWO bottom green arrows (Left Turn + Right Turn) with NO redundant straight circle!
    east_head = """
    Pose {
      translation 0.45 0.0 3.4
      rotation 0 0 1 -1.5707963
      children [
        # Housing Box (Clean 4-aspect dual-turn housing)
        Shape {
          appearance PBRAppearance { baseColor 0.08 0.08 0.09 roughness 0.4 metalness 0.8 }
          geometry Box { size 0.54 0.22 1.25 }
        }
        Pose {
          translation 0 0.115 0
          children [
            Shape {
              appearance PBRAppearance { baseColor 0.95 0.75 0.05 roughness 0.2 metalness 0.1 }
              geometry Box { size 0.60 0.015 1.32 }
            }
          ]
        }
        # Red
        Pose {
          translation 0.0 0.125 0.38
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
        Pose {
          translation 0.0 0.125 0.12
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
        # 1. Free-Left Turn Arrow (Driver's Left / Southbound: +0.14)
        Pose {
          translation 0.14 0.125 -0.14
          rotation 1 0 0 1.5708
          children [
            Shape {
              appearance DEF MAT_41_EAST_LEFT PBRAppearance {
                baseColor 0.02 0.2 0.05 emissiveColor 0.05 1.0 0.2 roughness 0.1 metalness 0.0
              }
              geometry Cylinder { height 0.015 radius 0.095 }
            }
          ]
        }
        # 2. Protected Right Turn Arrow (Driver's Right / Northbound: -0.14)
        Pose {
          translation -0.14 0.125 -0.14
          rotation 1 0 0 1.5708
          children [
            Shape {
              appearance DEF MAT_41_EAST_RIGHT PBRAppearance {
                baseColor 0.02 0.2 0.05 emissiveColor 0.0 0.0 0.0 roughness 0.1 metalness 0.0
              }
              geometry Cylinder { height 0.015 radius 0.095 }
            }
          ]
        }
      ]
    }
    """

    return f"""
# ==============================================================================
# CLEAN T-JUNCTION 3-WAY INDIAN TRAFFIC LIGHT POST: TRAFFIC_LIGHT_JUNCTION_41
# ==============================================================================
DEF TRAFFIC_LIGHT_JUNCTION_41 Robot {{
  translation -45.0 4.5 0.0
  rotation 0 0 1 0.0
  children [
    # 1. Concrete Base Island
    Pose {{
      translation 0 0 0.12
      children [
        Shape {{
          appearance PBRAppearance {{ baseColor 0.15 0.15 0.16 roughness 0.8 metalness 0.1 }}
          geometry Cylinder {{ height 0.24 radius 1.1 }}
        }}
      ]
    }}
    # Yellow Reflective Ring
    Pose {{
      translation 0 0 0.14
      children [
        Shape {{
          appearance PBRAppearance {{ baseColor 0.95 0.75 0.05 roughness 0.3 metalness 0.1 }}
          geometry Cylinder {{ height 0.26 radius 1.12 }}
        }}
      ]
    }}
    # 2. Sleek Center Mast
    Pose {{
      translation 0 0 2.2
      children [
        Shape {{
          appearance PBRAppearance {{ baseColor 0.08 0.08 0.09 roughness 0.3 metalness 0.9 }}
          geometry Cylinder {{ height 4.2 radius 0.09 }}
        }}
      ]
    }}
    # 3. Dedicated Directional Heads
    {north_head}
    {south_head}
    {east_head}
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

idx = wbt.find('DEF TRAFFIC_LIGHT_JUNCTION_41 Robot {')
if idx != -1:
    base_wbt = wbt[:idx]
else:
    idx27 = wbt.find('name "traffic_light_junction_27"')
    idx_end = wbt.find('locked TRUE\n}', idx27)
    base_wbt = wbt[:idx_end + len('locked TRUE\n}')]

new_post = generate_clean_t_junction_post()
final_wbt = base_wbt.rstrip() + "\n\n" + new_post.strip() + "\n"

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(final_wbt)

print(f"Configured clean 2-arrow merging face on East head in {WBT_PATH}")
