import re
import xml.etree.ElementTree as ET

# 1. Update sumo.net.xml tlLogic for Junction 41 with synchronized 28s cycle
NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

for tl in root.findall('tlLogic'):
    if tl.get('id') == '41':
        for p in list(tl.findall('phase')):
            tl.remove(p)
        ET.SubElement(tl, 'phase', {'duration': '12', 'state': 'GGgGGg'}) # 0-12s: North-South Straight Green + Left
        ET.SubElement(tl, 'phase', {'duration': '2',  'state': 'yygGGg'}) # 12-14s: Yellow
        ET.SubElement(tl, 'phase', {'duration': '12', 'state': 'rrgGGg'}) # 14-26s: Shortcut Merging Green
        ET.SubElement(tl, 'phase', {'duration': '2',  'state': 'yygGGg'}) # 26-28s: Yellow

tree.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print(f"Updated tlLogic 41 in {NET_PATH}")

# 2. Build tailored 3-way traffic light tower in Webots world
def generate_custom_3way_post():
    # South Face (Northbound on Road 23): Red, Amber, Straight Green, Right Arrow
    south_face = """
        Transform {
          translation 0.0 0.45 3.4
          rotation 0 0 1 0.0
          children [
            Shape {
              appearance PBRAppearance { baseColor 0.08 0.08 0.09 roughness 0.4 metalness 0.8 }
              geometry Box { size 0.38 0.22 1.15 }
            }
            Transform {
              translation 0 0.115 0
              children [
                Shape {
                  appearance PBRAppearance { baseColor 0.95 0.75 0.05 roughness 0.2 metalness 0.1 }
                  geometry Box { size 0.44 0.015 1.22 }
                }
              ]
            }
            # Red
            Transform {
              translation 0 0.125 0.34
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
              translation 0 0.125 0.10
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
              translation 0 0.125 -0.14
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
            # Right Turn Arrow
            Transform {
              translation -0.12 0.125 -0.36
              rotation 1 0 0 1.5708
              children [
                Shape {
                  appearance DEF MAT_41_SOUTH_RIGHT PBRAppearance {
                    baseColor 0.02 0.2 0.05 emissiveColor 0.0 0.0 0.0 roughness 0.1 metalness 0.0
                  }
                  geometry Cylinder { height 0.015 radius 0.075 }
                }
              ]
            }
          ]
        }
    """

    # North Face (Southbound on Road 23): Red, Amber, Straight Green (No Left Arrow)
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

    # East Face (Shortcut Merging Approach): Red, Amber, Green, Free-Left Arrow (South) & Right Arrow (North)
    east_face = """
        Transform {
          translation 0.45 0.0 3.4
          rotation 0 0 1 1.5707963
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
            # Green Straight
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
            # Free-Left Arrow (Merging South)
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
            # Right Turn Arrow (Merging North)
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
# TAILORED 3-WAY INDIAN TRAFFIC LIGHT MERGING POST: TRAFFIC_LIGHT_JUNCTION_41
# ==============================================================================
DEF TRAFFIC_LIGHT_JUNCTION_41 Robot {{
  translation -45.0 4.5 0.0
  rotation 0 0 1 0.0
  children [
    # 1. Concrete Island Base
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
    # 2. Sleek Central Mast
    Transform {{
      translation 0 0 2.2
      children [
        Shape {{
          appearance PBRAppearance {{ baseColor 0.08 0.08 0.09 roughness 0.3 metalness 0.9 }}
          geometry Cylinder {{ height 4.2 radius 0.09 }}
        }}
      ]
    }}
    # 3. Tailored Signal Faces
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

# Clean old 41 definitions
wbt = re.sub(r'# ==============================================================================\n# (?:SLEEK|TAILORED) 3-WAY INDIAN TRAFFIC LIGHT MERGING POST:[^#]*', '', wbt)
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

new_post = generate_custom_3way_post()
final_wbt = base_wbt.rstrip() + "\n\n" + new_post.strip() + "\n"

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(final_wbt)

print(f"Tailored 3-Way Traffic Light Island installed in {WBT_PATH}")
