import xml.etree.ElementTree as ET
import math

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"
CONTROLLER_FILE = r"f:\VEHDEMO\simulation\webots\controllers\pothole_controller\pothole_controller.py"

tree = ET.parse(NET_PATH)
root = tree.getroot()

lanes_by_id = {}
for lane in root.findall('.//lane'):
    l_id = lane.get('id')
    shape_str = lane.get('shape', '')
    if shape_str and not l_id.startswith(':'):
        pts = [tuple(map(float, p.split(','))) for p in shape_str.strip().split()]
        lanes_by_id[l_id] = pts

def get_point_along_lane(pts, frac):
    if len(pts) == 1:
        return pts[0]
    total_len = sum(math.hypot(pts[i+1][0]-pts[i][0], pts[i+1][1]-pts[i][1]) for i in range(len(pts)-1))
    target_d = total_len * frac
    acc = 0.0
    for i in range(len(pts)-1):
        seg_d = math.hypot(pts[i+1][0]-pts[i][0], pts[i+1][1]-pts[i][1])
        if acc + seg_d >= target_d:
            rem = (target_d - acc) / max(seg_d, 0.001)
            x = pts[i][0] + rem * (pts[i+1][0] - pts[i][0])
            y = pts[i][1] + rem * (pts[i+1][1] - pts[i][1])
            return (round(x, 2), round(y, 2))
        acc += seg_d
    return pts[-1]

target_lanes = [
    # 2-Lane Shortcut Road (Eastbound & Westbound)
    ('shortcut_east_0', 0.25, 0.90),
    ('shortcut_east_0', 0.70, 0.95),
    ('shortcut_west_0', 0.35, 0.90),
    ('shortcut_west_0', 0.75, 0.95),

    # Main Curved Boulevards
    ('0_0', 0.40, 0.90),
    ('0_1', 0.70, 0.95),
    ('7_0', 0.50, 0.90),
    ('6_1', 0.45, 0.95),
    ('5_0', 0.60, 0.90),
    ('4_1', 0.30, 0.95),
    ('-3_0', 0.55, 0.90),
    ('2_1', 0.65, 0.95),

    # Straight Arterial Avenues
    ('23_0', 0.35, 0.90),
    ('23_1', 0.70, 0.95),
    ('-8_0', 0.40, 0.90),
    ('-8_1', 0.80, 0.95),
    ('9_0', 0.50, 0.90),
    ('17_1', 0.45, 0.95),
]

POTHOLES = []
for idx, (lane_id, frac, rad) in enumerate(target_lanes):
    if lane_id in lanes_by_id:
        pt = get_point_along_lane(lanes_by_id[lane_id], frac)
        p_id = f"POTHOLE_{idx+1}"
        POTHOLES.append({
            'id': p_id,
            'lane': lane_id,
            'x': pt[0],
            'y': pt[1],
            'radius': rad
        })

# Distinct Terracotta Dirt Brown Color: baseColor 0.52 0.30 0.12
pothole_vrml_blocks = []
for p in POTHOLES:
    vrml = f"""DEF {p['id']} Solid {{
  translation {p['x']} {p['y']} 0.03
  rotation 0 0 1 0
  children [
    Shape {{
      appearance PBRAppearance {{
        baseColor 0.52 0.30 0.12
        roughness 0.95
        metalness 0
      }}
      geometry Cylinder {{
        height 0.025
        radius {p['radius']}
      }}
    }}
    Pose {{
      translation 0 0 0.012
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.32 0.16 0.06
            roughness 0.9
            metalness 0
          }}
          geometry Cylinder {{
            height 0.015
            radius {p['radius'] * 0.7:.2f}
          }}
        }}
      ]
    }}
  ]
  name "{p['id'].lower()}"
  locked TRUE
}}"""
    pothole_vrml_blocks.append(vrml)

pothole_supervisor_vrml = """DEF POTHOLE_SUPERVISOR Robot {
  name "pothole_supervisor"
  controller "pothole_controller"
  supervisor TRUE
  locked TRUE
}"""

with open(WBT_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Truncate cleanly after traffic_light_junction_43
cut_idx = -1
for i in range(len(lines)):
    if 'name "traffic_light_junction_43"' in lines[i]:
        for j in range(i, len(lines)):
            if lines[j].strip() == '}':
                cut_idx = j + 1
                break
        break

if cut_idx == -1:
    cut_idx = 7537

clean_base = "".join(lines[:cut_idx]).rstrip() + "\n\n"
full_wbt = clean_base + "\n\n".join(pothole_vrml_blocks) + "\n\n" + pothole_supervisor_vrml + "\n"

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(full_wbt)

print(f"Rebuilt {WBT_PATH} with {len(POTHOLES)} distinct Terracotta Brown Potholes strictly inside asphalt driving lanes!")

# Update Controller Code
py_potholes_repr = "POTHOLES = [\n"
for p in POTHOLES:
    py_potholes_repr += f"    {{'id': '{p['id']}', 'x': {p['x']}, 'y': {p['y']}, 'radius': {p['radius']}}},\n"
py_potholes_repr += "]\n"

pothole_code = f"""\"\"\"
pothole_controller.py — Brown Pothole Avoidance & Dynamic Go-Around Logic.
\"\"\"
import math
from controller import Supervisor

{py_potholes_repr}

def main():
    robot = Supervisor()
    timestep = int(robot.getBasicTimeStep())
    if timestep <= 0:
        timestep = 32

    root_children = robot.getRoot().getField("children")
    print(f"Brown Pothole Controller Online. Monitoring {{len(POTHOLES)}} potholes.")

    DETECTION_DIST = 16.0
    SWERVE_MAGNITUDE = 1.6
    SAFETY_GAP = 12.0

    while robot.step(timestep) != -1:
        n_children = root_children.getCount()
        vehicles = []

        for i in range(n_children):
            node = root_children.getMFNode(i)
            if node:
                name_field = node.getField("name")
                name = name_field.getSFString() if name_field else ""
                if "SUMO_VEHICLE" in name:
                    t_field = node.getField("translation")
                    r_field = node.getField("rotation")
                    if t_field and r_field:
                        pos = t_field.getSFVec3f()
                        rot = r_field.getSFRotation()
                        vehicles.append({{
                            'node': node,
                            'name': name,
                            't_field': t_field,
                            'r_field': r_field,
                            'pos': pos,
                            'rot': rot,
                        }})

        if not vehicles:
            continue

        for v in vehicles:
            vx, vy, vz = v['pos']
            v_rot = v['rot']
            
            heading = v_rot[3] if abs(v_rot[2]) > 0.5 else 0.0
            if v_rot[2] < 0:
                heading = -heading

            fwd_x = -math.sin(heading)
            fwd_y = math.cos(heading)
            lat_x = math.cos(heading)
            lat_y = math.sin(heading)

            for pot in POTHOLES:
                px, py = pot['x'], pot['y']
                dx = px - vx
                dy = py - vy
                dist = math.hypot(dx, dy)

                if 2.0 <= dist <= DETECTION_DIST:
                    dot_fwd = dx * fwd_x + dy * fwd_y
                    if dot_fwd > 1.5:
                        progress = 1.0 - (dist / DETECTION_DIST)

                        adjacent_free = True
                        for other_v in vehicles:
                            if other_v['name'] == v['name']:
                                continue
                            ox, oy, _ = other_v['pos']
                            o_dist = math.hypot(ox - vx, oy - vy)
                            if o_dist < SAFETY_GAP:
                                o_dx = ox - vx
                                o_dy = oy - vy
                                dot_lat = o_dx * lat_x + o_dy * lat_y
                                if abs(dot_lat) > 1.0 and abs(dot_lat) < 5.0:
                                    adjacent_free = False
                                    break

                        if adjacent_free:
                            swerve_scale = math.sin(progress * math.pi) * SWERVE_MAGNITUDE
                            offset_x = lat_x * swerve_scale * (timestep / 1000.0) * 1.5
                            offset_y = lat_y * swerve_scale * (timestep / 1000.0) * 1.5
                            v['t_field'].setSFVec3f([vx + offset_x, vy + offset_y, vz])
                        else:
                            pass

if __name__ == '__main__':
    main()
"""

with open(CONTROLLER_FILE, 'w', encoding='utf-8') as f:
    f.write(pothole_code)

print("Updated controller successfully!")
