import re

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"

with open(WBT_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove all old PedestrianCrossing proto nodes (which render yellow stripes)
content = re.sub(r'PedestrianCrossing\s*\{[^}]*\}', '', content)

# 2. Remove all startRoadsStartLine yellow texture references
content = re.sub(
    r'startRoadsStartLine\s*\[\s*"[^"]*yellow_crosswalk\.jpg"\s*\]',
    'startRoadsStartLine [ ]',
    content
)

# 3. Clean up any duplicate white crosswalk or pedestrian additions
idx = content.find("# --- CRISP WHITE ZEBRA CROSSWALK")
if idx == -1:
    idx = content.find("# --- ZEBRA CROSSWALK")
if idx == -1:
    idx = content.find("# ==============================================================================\n# UNBLOCKED 5-ASPECT")
if idx == -1:
    idx = content.find("# ==============================================================================")

base_world = content[:idx] if idx != -1 else content

def generate_crisp_white_zebra_vrml(name, tx, ty, rot_z):
    stripes = []
    for i in range(10):
        offset_x = -8.1 + (i * 1.8)
        stripes.append(f"""
            Transform {{
              translation {offset_x:.2f} 0 0.015
              children [
                Shape {{
                  appearance PBRAppearance {{
                    baseColor 0.98 0.98 0.98
                    roughness 0.2
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
# --- CRISP WHITE ZEBRA CROSSWALK: {name} ---
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
        size 19.0 3.8 0.01
      }}
    }}
    {"".join(stripes)}
  ]
  locked TRUE
}}
"""

def generate_pedestrian_node(name, init_x, init_y, rot_z, shirt_color):
    return f"""
# --- PEDESTRIAN: {name} ---
DEF {name.upper()} Pedestrian {{
  translation {init_x:.2f} {init_y:.2f} 1.27
  rotation 0 0 1 {rot_z}
  name "{name}"
  shirtColor {shirt_color}
  pantsColor 0.15 0.15 0.2
  shoesColor 0.1 0.1 0.1
  skinColor 0.8 0.6 0.45
}}
"""

crosswalks = [
    # Junction 25 (45.0, -45.0)
    generate_crisp_white_zebra_vrml("crosswalk_j25_north", 45.0, -33.5, 0.0),
    generate_crisp_white_zebra_vrml("crosswalk_j25_south", 45.0, -56.5, 0.0),
    generate_crisp_white_zebra_vrml("crosswalk_j25_east", 56.5, -45.0, 1.570796),
    generate_crisp_white_zebra_vrml("crosswalk_j25_west", 33.5, -45.0, 1.570796),

    # Junction 26 (-45.0, 45.0)
    generate_crisp_white_zebra_vrml("crosswalk_j26_north", -45.0, 56.5, 0.0),
    generate_crisp_white_zebra_vrml("crosswalk_j26_south", -45.0, 33.5, 0.0),
    generate_crisp_white_zebra_vrml("crosswalk_j26_east", -33.5, 45.0, 1.570796),
    generate_crisp_white_zebra_vrml("crosswalk_j26_west", -56.5, 45.0, 1.570796),

    # Junction 27 (105.0, 93.0)
    generate_crisp_white_zebra_vrml("crosswalk_j27_north", 105.0, 104.5, 0.0),
    generate_crisp_white_zebra_vrml("crosswalk_j27_south", 105.0, 81.5, 0.0),
    generate_crisp_white_zebra_vrml("crosswalk_j27_east", 116.5, 93.0, 1.570796),
    generate_crisp_white_zebra_vrml("crosswalk_j27_west", 93.5, 93.0, 1.570796),
]

pedestrians = [
    # Junction 26 Pedestrians (Placed cleanly on sidewalk curbs facing ACROSS the zebra crossing)
    generate_pedestrian_node("ped_j26_south", -55.0, 33.5, 0.0, "0.2 0.5 0.85"),
    generate_pedestrian_node("ped_j26_north", -35.0, 56.5, 3.14159, "0.85 0.3 0.2"),
    generate_pedestrian_node("ped_j26_east", -33.5, 35.0, 1.5708, "0.2 0.75 0.35"),
    generate_pedestrian_node("ped_j26_west", -56.5, 55.0, -1.5708, "0.75 0.65 0.15"),

    # Junction 25 Pedestrians
    generate_pedestrian_node("ped_j25_south", 35.0, -56.5, 0.0, "0.2 0.5 0.85"),
    generate_pedestrian_node("ped_j25_north", 55.0, -33.5, 3.14159, "0.85 0.3 0.2"),
    generate_pedestrian_node("ped_j25_east", 56.5, -55.0, 1.5708, "0.2 0.75 0.35"),
    generate_pedestrian_node("ped_j25_west", 33.5, -35.0, -1.5708, "0.75 0.65 0.15"),

    # Junction 27 Pedestrians
    generate_pedestrian_node("ped_j27_south", 95.0, 81.5, 0.0, "0.2 0.5 0.85"),
    generate_pedestrian_node("ped_j27_north", 115.0, 104.5, 3.14159, "0.85 0.3 0.2"),
    generate_pedestrian_node("ped_j27_east", 116.5, 83.0, 1.5708, "0.2 0.75 0.35"),
    generate_pedestrian_node("ped_j27_west", 93.5, 103.0, -1.5708, "0.75 0.65 0.15"),
]

ped_supervisor_node = """
# ==============================================================================
# PEDESTRIAN SIGNAL-OBEDIENT SUPERVISOR
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

print(f"Completely removed all yellow crosswalks and updated pedestrian facing orientations in {WBT_PATH}")
