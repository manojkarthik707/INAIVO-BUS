import re

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"

with open(WBT_PATH, 'r', encoding='utf-8') as f:
    wbt = f.read()

# Locate DEF TRAFFIC_LIGHT_JUNCTION_41
idx = wbt.find('DEF TRAFFIC_LIGHT_JUNCTION_41 Robot {')
if idx != -1:
    base_wbt = wbt[:idx]
else:
    # Find after junction 27
    idx27 = wbt.find('name "traffic_light_junction_27"')
    idx_end = wbt.find('locked TRUE\n}', idx27)
    base_wbt = wbt[:idx_end + len('locked TRUE\n}')]

# Define 3 prominent signal heads:
# 1. North Head (Mounted at Y=+0.45, facing North towards Southbound drivers, rot 0 0 1 0.0):
# Features LEFT turn arrow (driver's left: X = +0.14) for turning East into shortcut
north_head = """
    Pose {
      translation 0.0 0.45 3.4
      rotation 0 0 1 0.0
      children [
        # Housing Box (Wide 4-aspect housing)
        Shape {
          appearance PBRAppearance { baseColor 0.08 0.08 0.09 roughness 0.4 metalness 0.8 }
          geometry Box { size 0.54 0.22 1.25 }
        }
        # Yellow Border Frame
        Pose {
          translation 0 0.115 0
          children [
            Shape {
              appearance PBRAppearance { baseColor 0.95 0.75 0.05 roughness 0.2 metalness 0.1 }
              geometry Box { size 0.60 0.015 1.32 }
            }
          ]
        }
        # Red Lens
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
        # Amber Lens
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
        # Straight Green Lens
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
        # Prominent LEFT TURN ARROW (Turning East into Shortcut: Driver's Left = +0.16)
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

# 2. South Head (Mounted at Y=-0.45, facing South towards Northbound drivers, rot 0 0 1 3.1415926):
# Features RIGHT turn arrow (driver's right: local X = -0.16) for turning East into shortcut
south_head = """
    Pose {
      translation 0.0 -0.45 3.4
      rotation 0 0 1 3.1415926
      children [
        # Housing Box (Wide 4-aspect housing)
        Shape {
          appearance PBRAppearance { baseColor 0.08 0.08 0.09 roughness 0.4 metalness 0.8 }
          geometry Box { size 0.54 0.22 1.25 }
        }
        # Yellow Border Frame
        Pose {
          translation 0 0.115 0
          children [
            Shape {
              appearance PBRAppearance { baseColor 0.95 0.75 0.05 roughness 0.2 metalness 0.1 }
              geometry Box { size 0.60 0.015 1.32 }
            }
          ]
        }
        # Red Lens
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
        # Amber Lens
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
        # Straight Green Lens
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
        # Prominent RIGHT TURN ARROW (Turning East into Shortcut: Driver's Right = -0.16)
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

# 3. East Head (Mounted at X=+0.45, facing East towards Shortcut drivers, rot 0 0 1 -1.5707963):
# Features Free-Left Arrow (Driver's Left = +0.18) and Protected Right Arrow (Driver's Right = -0.18)
east_head = """
    Pose {
      translation 0.45 0.0 3.4
      rotation 0 0 1 -1.5707963
      children [
        # Housing Box (Wide 5-aspect housing)
        Shape {
          appearance PBRAppearance { baseColor 0.08 0.08 0.09 roughness 0.4 metalness 0.8 }
          geometry Box { size 0.64 0.22 1.25 }
        }
        # Yellow Border Frame
        Pose {
          translation 0 0.115 0
          children [
            Shape {
              appearance PBRAppearance { baseColor 0.95 0.75 0.05 roughness 0.2 metalness 0.1 }
              geometry Box { size 0.70 0.015 1.32 }
            }
          ]
        }
        # Red Lens
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
        # Amber Lens
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
        # Straight / Merging Green Lens
        Pose {
          translation 0.0 0.125 -0.14
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
        # Free-Left Arrow (Driver's Left / Southbound: +0.18)
        Pose {
          translation 0.18 0.125 -0.14
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
        # Right Turn Arrow (Driver's Right / Northbound: -0.18)
        Pose {
          translation -0.18 0.125 -0.14
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

full_robot = f"""
# ==============================================================================
# PROMINENT DIRECTIONAL 3-WAY INDIAN TRAFFIC LIGHT POST: TRAFFIC_LIGHT_JUNCTION_41
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
    # 3. Prominent Directional Signal Heads
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

new_wbt = base_wbt.rstrip() + "\n\n" + full_robot.strip() + "\n"

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(new_wbt)

print(f"Installed prominent directional turn signal heads on Junction 41 in {WBT_PATH}")
