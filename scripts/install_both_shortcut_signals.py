import re
import xml.etree.ElementTree as ET

# 1. Update sumo.net.xml tlLogic for Junction 43 with synchronized 28s cycle
NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

for tl in root.findall('tlLogic'):
    if tl.get('id') == '43':
        for p in list(tl.findall('phase')):
            tl.remove(p)
        ET.SubElement(tl, 'phase', {'duration': '12', 'state': 'GGgGGg'}) # 0-12s: North-South Straight Green + Turn
        ET.SubElement(tl, 'phase', {'duration': '2',  'state': 'yygGGg'}) # 12-14s: Yellow
        ET.SubElement(tl, 'phase', {'duration': '12', 'state': 'rrgGGg'}) # 14-26s: Shortcut Merging Green
        ET.SubElement(tl, 'phase', {'duration': '2',  'state': 'yygGGg'}) # 26-28s: Yellow

tree.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print(f"Updated tlLogic 43 in {NET_PATH}")

# 2. Build Junction 43 Traffic Light Post at (+45.0, 4.5)
def generate_junction_43_post():
    # North Head (Southbound on Road 6): rot 0 0 1 0.0
    # Red, Amber, Straight Green + RIGHT Turn Arrow (turning West into shortcut: Driver's Right = -0.16)
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
          translation 0.05 0.125 0.38
          rotation 1 0 0 1.5708
          children [
            Shape {
              appearance DEF MAT_43_NORTH_RED PBRAppearance {
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
              appearance DEF MAT_43_NORTH_AMBER PBRAppearance {
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
              appearance DEF MAT_43_NORTH_STRAIGHT PBRAppearance {
                baseColor 0.02 0.2 0.05 emissiveColor 0.0 0.0 0.0 roughness 0.1 metalness 0.0
              }
              geometry Cylinder { height 0.015 radius 0.11 }
            }
          ]
        }
        # Right Turn Arrow (Turning West into Shortcut: Driver's Right = -0.16)
        Pose {
          translation -0.16 0.125 -0.14
          rotation 1 0 0 1.5708
          children [
            Shape {
              appearance DEF MAT_43_NORTH_RIGHT PBRAppearance {
                baseColor 0.02 0.2 0.05 emissiveColor 0.05 1.0 0.2 roughness 0.1 metalness 0.0
              }
              geometry Cylinder { height 0.015 radius 0.095 }
            }
          ]
        }
      ]
    }
    """

    # South Head (Northbound on Road 5): rot 0 0 1 3.1415926
    # Red, Amber, Straight Green + LEFT Turn Arrow (turning West into shortcut: Driver's Left = +0.16 in local rot)
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
          translation -0.05 0.125 0.38
          rotation 1 0 0 1.5708
          children [
            Shape {
              appearance DEF MAT_43_SOUTH_RED PBRAppearance {
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
              appearance DEF MAT_43_SOUTH_AMBER PBRAppearance {
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
              appearance DEF MAT_43_SOUTH_STRAIGHT PBRAppearance {
                baseColor 0.02 0.2 0.05 emissiveColor 0.0 0.0 0.0 roughness 0.1 metalness 0.0
              }
              geometry Cylinder { height 0.015 radius 0.11 }
            }
          ]
        }
        # Left Turn Arrow (Turning West into Shortcut: Driver's Left = +0.16)
        Pose {
          translation 0.16 0.125 -0.14
          rotation 1 0 0 1.5708
          children [
            Shape {
              appearance DEF MAT_43_SOUTH_LEFT PBRAppearance {
                baseColor 0.02 0.2 0.05 emissiveColor 0.05 1.0 0.2 roughness 0.1 metalness 0.0
              }
              geometry Cylinder { height 0.015 radius 0.095 }
            }
          ]
        }
      ]
    }
    """

    # West Head (Facing West towards Eastbound shortcut traffic: rot 0 0 1 1.5707963, mounted at X=-0.45)
    # Turn options: Left Arrow (North onto Road 5) + Right Arrow (South onto Road 6)
    west_head = """
    Pose {
      translation -0.45 0.0 3.4
      rotation 0 0 1 1.5707963
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
          translation 0.0 0.125 0.38
          rotation 1 0 0 1.5708
          children [
            Shape {
              appearance DEF MAT_43_WEST_RED PBRAppearance {
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
              appearance DEF MAT_43_WEST_AMBER PBRAppearance {
                baseColor 0.2 0.18 0.02 emissiveColor 0.0 0.0 0.0 roughness 0.1 metalness 0.0
              }
              geometry Cylinder { height 0.015 radius 0.11 }
            }
          ]
        }
        # Free-Left Turn Arrow (Driver's Left / Northbound: +0.14)
        Pose {
          translation 0.14 0.125 -0.14
          rotation 1 0 0 1.5708
          children [
            Shape {
              appearance DEF MAT_43_WEST_LEFT PBRAppearance {
                baseColor 0.02 0.2 0.05 emissiveColor 0.05 1.0 0.2 roughness 0.1 metalness 0.0
              }
              geometry Cylinder { height 0.015 radius 0.095 }
            }
          ]
        }
        # Right Turn Arrow (Driver's Right / Southbound: -0.14)
        Pose {
          translation -0.14 0.125 -0.14
          rotation 1 0 0 1.5708
          children [
            Shape {
              appearance DEF MAT_43_WEST_RIGHT PBRAppearance {
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
# PROMINENT 3-WAY INDIAN TRAFFIC LIGHT MERGING POST: TRAFFIC_LIGHT_JUNCTION_43
# ==============================================================================
DEF TRAFFIC_LIGHT_JUNCTION_43 Robot {{
  translation 45.0 4.5 0.0
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
    {west_head}
  ]
  name "traffic_light_junction_43"
  controller "traffic_light_controller"
  supervisor TRUE
  locked TRUE
}}
"""

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"
with open(WBT_PATH, 'r', encoding='utf-8') as f:
    wbt = f.read()

# Clean old 43 definitions
wbt = re.sub(r'# ==============================================================================\n# PROMINENT 3-WAY INDIAN TRAFFIC LIGHT MERGING POST: TRAFFIC_LIGHT_JUNCTION_43[^#]*', '', wbt)
wbt = re.sub(r'DEF TRAFFIC_LIGHT_JUNCTION_43 Robot \{[^}]*(?:\{[^}]*\}[^}]*)*\}', '', wbt)

new_post_43 = generate_junction_43_post()
final_wbt = wbt.rstrip() + "\n\n" + new_post_43.strip() + "\n"

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(final_wbt)

print(f"Successfully installed TRAFFIC_LIGHT_JUNCTION_43 at (45.0, 4.5) in {WBT_PATH}")
