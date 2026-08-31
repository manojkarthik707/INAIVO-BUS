import os
import re

def generate_zebra_crossing_vrml(name, tx, ty, rot_z):
    stripes = []
    for i in range(11):
        offset_x = -9.0 + (i * 1.8)
        stripes.append(f"""
            Transform {{
              translation {offset_x:.2f} 0 0.015
              children [
                Shape {{
                  appearance PBRAppearance {{
                    baseColor 0.95 0.95 0.95
                    roughness 0.3
                    metalness 0.05
                  }}
                  geometry Box {{
                    size 0.95 3.4 0.01
                  }}
                }}
              ]
            }}
        """)

    return f"""
# --- ZEBRA CROSSWALK: {name} ---
Solid {{
  name "{name}"
  translation {tx:.2f} {ty:.2f} 0.02
  rotation 0 0 1 {rot_z}
  children [
    Shape {{
      appearance PBRAppearance {{
        baseColor 0.12 0.12 0.14
        roughness 0.8
        metalness 0.0
      }}
      geometry Box {{
        size 20.5 3.8 0.01
      }}
    }}
    {"".join(stripes)}
  ]
  locked TRUE
}}
"""

def generate_animated_pedestrian_vrml(name, start_x, start_y):
    return f"""
# --- PEDESTRIAN WALKER: {name} ---
DEF {name.upper()} Pedestrian {{
  translation {start_x:.2f} {start_y:.2f} 1.27
  name "{name}"
  shirtColor 0.2 0.5 0.85
  pantsColor 0.15 0.15 0.2
  shoesColor 0.1 0.1 0.1
  skinColor 0.8 0.6 0.45
}}
"""

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"

with open(WBT_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("# ==============================================================================\n# SLEEK 4-WAY INDIAN TRAFFIC LIGHT POST")
if idx == -1:
    idx = content.find("# ==============================================================================\n# UNBLOCKED 5-ASPECT")
if idx == -1:
    idx = content.find("# ==============================================================================")

base_world = content[:idx] if idx != -1 else content

crosswalks = [
    # Junction 25 (45.0, -45.0)
    generate_zebra_crossing_vrml("crosswalk_j25_north", 45.0, -33.5, 0.0),
    generate_zebra_crossing_vrml("crosswalk_j25_south", 45.0, -56.5, 0.0),
    generate_zebra_crossing_vrml("crosswalk_j25_east", 56.5, -45.0, 1.570796),
    generate_zebra_crossing_vrml("crosswalk_j25_west", 33.5, -45.0, 1.570796),

    # Junction 26 (-45.0, 45.0)
    generate_zebra_crossing_vrml("crosswalk_j26_north", -45.0, 56.5, 0.0),
    generate_zebra_crossing_vrml("crosswalk_j26_south", -45.0, 33.5, 0.0),
    generate_zebra_crossing_vrml("crosswalk_j26_east", -33.5, 45.0, 1.570796),
    generate_zebra_crossing_vrml("crosswalk_j26_west", -56.5, 45.0, 1.570796),

    # Junction 27 (105.0, 93.0)
    generate_zebra_crossing_vrml("crosswalk_j27_north", 105.0, 104.5, 0.0),
    generate_zebra_crossing_vrml("crosswalk_j27_south", 105.0, 81.5, 0.0),
    generate_zebra_crossing_vrml("crosswalk_j27_east", 116.5, 93.0, 1.570796),
    generate_zebra_crossing_vrml("crosswalk_j27_west", 93.5, 93.0, 1.570796),
]

pedestrians = [
    generate_animated_pedestrian_vrml("ped_j25_north_1", 45.0, -33.5),
    generate_animated_pedestrian_vrml("ped_j25_south_1", 45.0, -56.5),
    generate_animated_pedestrian_vrml("ped_j25_east_1", 56.5, -45.0),
    generate_animated_pedestrian_vrml("ped_j26_south_1", -45.0, 33.5),
    generate_animated_pedestrian_vrml("ped_j26_north_1", -45.0, 56.5),
    generate_animated_pedestrian_vrml("ped_j26_west_1", -56.5, 45.0),
    generate_animated_pedestrian_vrml("ped_j27_north_1", 105.0, 104.5),
    generate_animated_pedestrian_vrml("ped_j27_south_1", 105.0, 81.5),
]

ped_supervisor_node = """
# ==============================================================================
# PEDESTRIAN CROSSING CONTROLLER SUPERVISOR
# ==============================================================================
DEF PEDESTRIAN_SUPERVISOR Robot {
  name "pedestrian_supervisor"
  controller "pedestrian_controller"
  supervisor TRUE
  locked TRUE
}
"""

from rebuild_5aspect_working_traffic_lights import generate_clean_4way_vrml

tls_nodes = [
    generate_clean_4way_vrml("TRAFFIC_LIGHT_JUNCTION_25", "25", 45.0, -45.0),
    generate_clean_4way_vrml("TRAFFIC_LIGHT_JUNCTION_26", "26", -45.0, 45.0),
    generate_clean_4way_vrml("TRAFFIC_LIGHT_JUNCTION_27", "27", 105.0, 93.0),
]

new_wbt = base_world.rstrip() + "\n\n" + "\n".join(crosswalks) + "\n\n" + "\n".join(pedestrians) + "\n\n" + ped_supervisor_node + "\n\n" + "\n".join(tls_nodes) + "\n"

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(new_wbt)

print(f"Integrated 12 Zebra Crosswalks, 8 Pedestrians, Pedestrian Supervisor, and 3 4-Way Traffic Light Towers in {WBT_PATH}")
