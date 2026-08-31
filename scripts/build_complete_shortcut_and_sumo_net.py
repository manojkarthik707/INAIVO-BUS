import xml.etree.ElementTree as ET
import re

# 1. Update sumo.net.xml to add shortcut road edges between Junction 41 (-45, 4.5 -> SUMO 130, 183) and Junction 43 (45, 4.5 -> SUMO 220, 192)
NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

# Check if shortcut edges already exist
existing_edge_ids = [e.get('id') for e in root.findall('edge')]

if 'shortcut_east' not in existing_edge_ids:
    # Edge from J41 to J43 (West to East)
    edge_e = ET.Element('edge', {
        'id': 'shortcut_east',
        'from': '41',
        'to': '43',
        'priority': '10',
        'type': 'highway.city'
    })
    lane_e0 = ET.SubElement(edge_e, 'lane', {
        'id': 'shortcut_east_0',
        'index': '0',
        'speed': '18.00',
        'length': '88.00',
        'width': '3.75',
        'shape': '133.00,181.50 217.00,190.50'
    })
    lane_e1 = ET.SubElement(edge_e, 'lane', {
        'id': 'shortcut_east_1',
        'index': '1',
        'speed': '18.00',
        'length': '88.00',
        'width': '3.75',
        'shape': '133.00,184.75 217.00,193.75'
    })
    root.insert(len(root.findall('edge')), edge_e)

if 'shortcut_west' not in existing_edge_ids:
    # Edge from J43 to J41 (East to West)
    edge_w = ET.Element('edge', {
        'id': 'shortcut_west',
        'from': '43',
        'to': '41',
        'priority': '10',
        'type': 'highway.city'
    })
    lane_w0 = ET.SubElement(edge_w, 'lane', {
        'id': 'shortcut_west_0',
        'index': '0',
        'speed': '18.00',
        'length': '88.00',
        'width': '3.75',
        'shape': '217.00,193.50 133.00,184.50'
    })
    lane_w1 = ET.SubElement(edge_w, 'lane', {
        'id': 'shortcut_west_1',
        'index': '1',
        'speed': '18.00',
        'length': '88.00',
        'width': '3.75',
        'shape': '217.00,190.25 133.00,181.25'
    })
    root.insert(len(root.findall('edge')), edge_w)

# Update tlLogic id="41" with 28s deterministic static cycle (14s Main Green, 14s Shortcut Green)
for tl in root.findall('tlLogic'):
    if tl.get('id') == '41':
        root.remove(tl)

tl41 = ET.SubElement(root, 'tlLogic', {
    'id': '41',
    'type': 'static',
    'programID': '0',
    'offset': '0'
})
ET.SubElement(tl41, 'phase', {'duration': '12', 'state': 'GGgGGg'})
ET.SubElement(tl41, 'phase', {'duration': '2',  'state': 'yygyyg'})
ET.SubElement(tl41, 'phase', {'duration': '12', 'state': 'rrgrrg'})
ET.SubElement(tl41, 'phase', {'duration': '2',  'state': 'yygyyg'})

tree.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print(f"Updated SUMO network with shortcut edges and 28s traffic light 41 in {NET_PATH}")

# 2. Build Webots 3-Way Merging Post at (-45.0, 4.5) with tailored signal faces
def generate_custom_3way_tower(def_name, j_id, tx, ty):
    # Face 1: South (Northbound traffic): Red, Amber, Straight Green, Right Turn Arrow
    south_face = f"""
        Transform {{
          translation 0.0 0.45 3.4
          rotation 0 0 1 0.0
          children [
            Shape {{
              appearance PBRAppearance {{ baseColor 0.08 0.08 0.09 roughness 0.4 metalness 0.8 }}
              geometry Box {{ size 0.38 0.22 1.15 }}
            }}
            Transform {{
              translation 0 0.115 0
              children [
                Shape {{
                  appearance PBRAppearance {{ baseColor 0.95 0.75 0.05 roughness 0.2 metalness 0.1 }}
                  geometry Box {{ size 0.44 0.015 1.22 }}
                }}
              ]
            }}
            # 1. Red Lens
            Transform {{
              translation 0 0.125 0.34
              rotation 1 0 0 1.5708
              children [
                Shape {{
                  appearance DEF MAT_{j_id}_SOUTH_RED PBRAppearance {{
                    baseColor 0.2 0.02 0.02 emissiveColor 1.0 0.05 0.05 roughness 0.1 metalness 0.0
                  }}
                  geometry Cylinder {{ height 0.015 radius 0.11 }}
                }}
              ]
            }}
            # 2. Amber Lens
            Transform {{
              translation 0 0.125 0.10
              rotation 1 0 0 1.5708
              children [
                Shape {{
                  appearance DEF MAT_{j_id}_SOUTH_AMBER PBRAppearance {{
                    baseColor 0.2 0.18 0.02 emissiveColor 0.0 0.0 0.0 roughness 0.1 metalness 0.0
                  }}
                  geometry Cylinder {{ height 0.015 radius 0.11 }}
                }}
              ]
            }}
            # 3. Straight Green Lens
            Transform {{
              translation 0 0.125 -0.14
              rotation 1 0 0 1.5708
              children [
                Shape {{
                  appearance DEF MAT_{j_id}_SOUTH_STRAIGHT PBRAppearance {{
                    baseColor 0.02 0.2 0.05 emissiveColor 0.0 0.0 0.0 roughness 0.1 metalness 0.0
                  }}
                  geometry Cylinder {{ height 0.015 radius 0.11 }}
                }}
              ]
            }}
            # 4. Right Turn Arrow (Turning East into shortcut road)
            Transform {{
              translation -0.12 0.125 -0.36
              rotation 1 0 0 1.5708
              children [
                Shape {{
                  appearance DEF MAT_{j_id}_SOUTH_RIGHT PBRAppearance {{
                    baseColor 0.02 0.2 0.05 emissiveColor 0.0 0.0 0.0 roughness 0.1 metalness 0.0
                  }}
                  geometry Cylinder {{ height 0.015 radius 0.075 }}
                }}
              ]
            }}
          ]
        }}
    """

    # Face 2: North (Southbound traffic): Red, Amber, Straight Green, Free Left Arrow
    north_face = f"""
        Transform {{
          translation 0.0 -0.45 3.4
          rotation 0 0 1 3.1415926
          children [
            Shape {{
              appearance PBRAppearance {{ baseColor 0.08 0.08 0.09 roughness 0.4 metalness 0.8 }}
              geometry Box {{ size 0.38 0.22 1.15 }}
            }}
            Transform {{
              translation 0 0.115 0
              children [
                Shape {{
                  appearance PBRAppearance {{ baseColor 0.95 0.75 0.05 roughness 0.2 metalness 0.1 }}
                  geometry Box {{ size 0.44 0.015 1.22 }}
                }}
              ]
            }}
            # 1. Red Lens
            Transform {{
              translation 0 0.125 0.34
              rotation 1 0 0 1.5708
              children [
                Shape {{
                  appearance DEF MAT_{j_id}_NORTH_RED PBRAppearance {{
                    baseColor 0.2 0.02 0.02 emissiveColor 1.0 0.05 0.05 roughness 0.1 metalness 0.0
                  }}
                  geometry Cylinder {{ height 0.015 radius 0.11 }}
                }}
              ]
            }}
            # 2. Amber Lens
            Transform {{
              translation 0 0.125 0.10
              rotation 1 0 0 1.5708
              children [
                Shape {{
                  appearance DEF MAT_{j_id}_NORTH_AMBER PBRAppearance {{
                    baseColor 0.2 0.18 0.02 emissiveColor 0.0 0.0 0.0 roughness 0.1 metalness 0.0
                  }}
                  geometry Cylinder {{ height 0.015 radius 0.11 }}
                }}
              ]
            }}
            # 3. Straight Green Lens
            Transform {{
              translation 0 0.125 -0.14
              rotation 1 0 0 1.5708
              children [
                Shape {{
                  appearance DEF MAT_{j_id}_NORTH_STRAIGHT PBRAppearance {{
                    baseColor 0.02 0.2 0.05 emissiveColor 0.0 0.0 0.0 roughness 0.1 metalness 0.0
                  }}
                  geometry Cylinder {{ height 0.015 radius 0.11 }}
                }}
              ]
            }}
            # 4. Free-Left Arrow (Left side from driver perspective: X = +0.12, turning East into shortcut)
            Transform {{
              translation 0.12 0.125 -0.36
              rotation 1 0 0 1.5708
              children [
                Shape {{
                  appearance DEF MAT_{j_id}_NORTH_LEFT PBRAppearance {{
                    baseColor 0.02 0.2 0.05 emissiveColor 0.05 1.0 0.2 roughness 0.1 metalness 0.0
                  }}
                  geometry Cylinder {{ height 0.015 radius 0.075 }}
                }}
              ]
            }}
          ]
        }}
    """

    # Face 3: East (Merging Shortcut Traffic): Red, Amber, Green, Free-Left Arrow (South) & Right Arrow (North)
    east_face = f"""
        Transform {{
          translation 0.45 0.0 3.4
          rotation 0 0 1 1.5707963
          children [
            Shape {{
              appearance PBRAppearance {{ baseColor 0.08 0.08 0.09 roughness 0.4 metalness 0.8 }}
              geometry Box {{ size 0.38 0.22 1.25 }}
            }}
            Transform {{
              translation 0 0.115 0
              children [
                Shape {{
                  appearance PBRAppearance {{ baseColor 0.95 0.75 0.05 roughness 0.2 metalness 0.1 }}
                  geometry Box {{ size 0.44 0.015 1.32 }}
                }}
              ]
            }}
            # 1. Red Lens
            Transform {{
              translation 0 0.125 0.38
              rotation 1 0 0 1.5708
              children [
                Shape {{
                  appearance DEF MAT_{j_id}_EAST_RED PBRAppearance {{
                    baseColor 0.2 0.02 0.02 emissiveColor 1.0 0.05 0.05 roughness 0.1 metalness 0.0
                  }}
                  geometry Cylinder {{ height 0.015 radius 0.11 }}
                }}
              ]
            }}
            # 2. Amber Lens
            Transform {{
              translation 0 0.125 0.12
              rotation 1 0 0 1.5708
              children [
                Shape {{
                  appearance DEF MAT_{j_id}_EAST_AMBER PBRAppearance {{
                    baseColor 0.2 0.18 0.02 emissiveColor 0.0 0.0 0.0 roughness 0.1 metalness 0.0
                  }}
                  geometry Cylinder {{ height 0.015 radius 0.11 }}
                }}
              ]
            }}
            # 3. Green Lens
            Transform {{
              translation 0 0.125 -0.14
              rotation 1 0 0 1.5708
              children [
                Shape {{
                  appearance DEF MAT_{j_id}_EAST_STRAIGHT PBRAppearance {{
                    baseColor 0.02 0.2 0.05 emissiveColor 0.0 0.0 0.0 roughness 0.1 metalness 0.0
                  }}
                  geometry Cylinder {{ height 0.015 radius 0.11 }}
                }}
              ]
            }}
            # 4. Free-Left Arrow (Merging South onto Road 23)
            Transform {{
              translation 0.14 0.125 -0.38
              rotation 1 0 0 1.5708
              children [
                Shape {{
                  appearance DEF MAT_{j_id}_EAST_LEFT PBRAppearance {{
                    baseColor 0.02 0.2 0.05 emissiveColor 0.05 1.0 0.2 roughness 0.1 metalness 0.0
                  }}
                  geometry Cylinder {{ height 0.015 radius 0.075 }}
                }}
              ]
            }}
            # 5. Right Turn Arrow (Merging North onto Road 23)
            Transform {{
              translation -0.14 0.125 -0.38
              rotation 1 0 0 1.5708
              children [
                Shape {{
                  appearance DEF MAT_{j_id}_EAST_RIGHT PBRAppearance {{
                    baseColor 0.02 0.2 0.05 emissiveColor 0.0 0.0 0.0 roughness 0.1 metalness 0.0
                  }}
                  geometry Cylinder {{ height 0.015 radius 0.075 }}
                }}
              ]
            }}
          ]
        }}
    """

    return f"""
# ==============================================================================
# TAILORED 3-WAY INDIAN TRAFFIC LIGHT MERGING POST: {def_name}
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
          appearance PBRAppearance {{ baseColor 0.15 0.15 0.16 roughness 0.8 metalness 0.1 }}
          geometry Cylinder {{ height 0.24 radius 1.1 }}
        }}
      ]
    }}
    # Yellow Base Ring
    Transform {{
      translation 0 0 0.14
      children [
        Shape {{
          appearance PBRAppearance {{ baseColor 0.95 0.75 0.05 roughness 0.3 metalness 0.1 }}
          geometry Cylinder {{ height 0.26 radius 1.12 }}
        }}
      ]
    }}
    # 2. Sleek Mast
    Transform {{
      translation 0 0 2.2
      children [
        Shape {{
          appearance PBRAppearance {{ baseColor 0.08 0.08 0.09 roughness 0.3 metalness 0.9 }}
          geometry Cylinder {{ height 4.2 radius 0.09 }}
        }}
      ]
    }}
    # 3. Tailored 3-Way Signal Heads
    {south_face}
    {north_face}
    {east_face}
  ]
  name "traffic_light_junction_{j_id}"
  controller "traffic_light_controller"
  supervisor TRUE
  locked TRUE
}}
"""

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"
with open(WBT_PATH, 'r', encoding='utf-8') as f:
    wbt_content = f.read()

# Clean old post and append tailored 3-way post
wbt_content = re.sub(r'# ==============================================================================\n# (?:SLEEK|TAILORED) 3-WAY INDIAN TRAFFIC LIGHT MERGING POST:[^#]*', '', wbt_content)
wbt_content = re.sub(r'DEF TRAFFIC_LIGHT_JUNCTION_41 Robot \{[^}]*(?:\{[^}]*\}[^}]*)*\}', '', wbt_content)

post_vrml = generate_custom_3way_tower("TRAFFIC_LIGHT_JUNCTION_41", "41", -45.0, 4.5)
wbt_content = wbt_content.rstrip() + "\n\n" + post_vrml + "\n"

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(wbt_content)

print("Tailored 3-Way Traffic Light Island successfully integrated in Webots world.")
