"""
pothole_controller.py — Dynamic Pothole Swerve & 3D High-Security Indian License Plate Supervisor.

Features:
1. Guaranteed 3D Indian Number Plates on EVERY Vehicle & Bike:
   - Dynamically mounts crisp 3D front & rear license plates to every car, bus, sprinter van, motorcycle, and scooter.
   - Front Plate: Clean white HSRP plate with bold black Indian registration text.
   - Rear Plate: Clean white HSRP plate with bold black Indian registration text.
   - 100% unique registration numbers across all 100 vehicles (TN, KA, MH, DL, TS, GJ, KL, AP, WB, HR).
2. Dynamic Motion-Vector Pothole Swerve:
   - Seamless 1.8m sinusoidal swerve into free adjacent lane when approaching brown potholes.
"""

import math, re
from controller import Supervisor

INDIAN_STATES = ["TN", "KA", "MH", "DL", "TS", "GJ", "KL", "AP", "WB", "HR"]
SERIES = ["AB", "CD", "EF", "GH", "JK", "LM", "NP", "QR", "ST", "UV", "WX", "YZ"]

def get_unique_indian_plate(v_idx):
    state = INDIAN_STATES[v_idx % len(INDIAN_STATES)]
    rto = f"{(v_idx * 3 + 1) % 99 + 1:02d}"
    series = SERIES[(v_idx // len(INDIAN_STATES)) % len(SERIES)]
    num = f"{(v_idx * 127 + 1001) % 9000 + 1000:04d}"
    return f"{state} {rto} {series} {num}"

def create_plate_vrml(plate_str, is_front, v_type):
    # Determine mount offsets based on vehicle chassis dimensions
    if "bus" in v_type:
        fwd_x = 2.95 if is_front else -4.10
        fwd_z = 0.45 if is_front else 0.58
    elif "sprinter" in v_type or "van" in v_type:
        fwd_x = 2.45 if is_front else -3.10
        fwd_z = 0.40 if is_front else 0.52
    elif "bike" in v_type or "scooter" in v_type or "motor" in v_type:
        fwd_x = 0.82 if is_front else -0.92
        fwd_z = 0.58 if is_front else 0.52
    else:
        # Standard Cars (Tesla, Prius, BMW, Citroen)
        fwd_x = 2.15 if is_front else -2.25
        fwd_z = 0.38 if is_front else 0.46

    # Heading rotation: Front faces forward (0 rad), Rear faces backward (pi rad = 3.14159 rad)
    rot_str = "0 0 1 0" if is_front else "0 0 1 3.14159"
    name_str = "plate_front" if is_front else "plate_rear"
    p_w = 0.48 if ("bike" in v_type or "scooter" in v_type) else 0.52
    p_h = 0.12

    vrml = f"""Solid {{
  translation {fwd_x} 0 {fwd_z}
  rotation {rot_str}
  children [
    Shape {{
      appearance PBRAppearance {{
        baseColor 0.96 0.96 0.96
        roughness 0.2
        metalness 0.05
      }}
      geometry Box {{
        size 0.02 {p_w} {p_h}
      }}
    }}
    Pose {{
      translation 0.015 0.22 -0.035
      rotation 0.57735 0.57735 -0.57735 2.0944
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.02 0.02 0.02
            roughness 0.1
            metalness 0
          }}
          geometry Text {{
            string [ "{plate_str}" ]
            fontStyle FontStyle {{
              size 0.068
              family "Arial"
              style "BOLD"
            }}
          }}
        }}
      ]
    }}
  ]
  name "{name_str}"
}}"""
    return vrml

POTHOLES = [
    # 2-Lane Shortcut Road
    {'id': 'POTHOLE_1', 'x': -13.14, 'y': 0.44,  'radius': 0.90},
    {'id': 'POTHOLE_2', 'x': 10.20,  'y': 2.78,  'radius': 0.95},
    {'id': 'POTHOLE_3', 'x': 7.96,   'y': -0.96, 'radius': 0.90},
    {'id': 'POTHOLE_4', 'x': -12.79, 'y': -3.03, 'radius': 0.95},

    # Main Curved Boulevards
    {'id': 'POTHOLE_5', 'x': -101.35,'y': 36.10, 'radius': 0.90},
    {'id': 'POTHOLE_6', 'x': -78.33, 'y': 45.37, 'radius': 0.95},
    {'id': 'POTHOLE_7', 'x': -15.01, 'y': 53.07, 'radius': 0.90},
    {'id': 'POTHOLE_8', 'x': 28.76,  'y': 40.22, 'radius': 0.95},
    {'id': 'POTHOLE_9', 'x': 53.07,  'y': -23.79,'radius': 0.90},
    {'id': 'POTHOLE_10','x': 45.36,  'y': -78.38,'radius': 0.95},
    {'id': 'POTHOLE_11','x': -33.44, 'y': -113.07,'radius': 0.90},
    {'id': 'POTHOLE_12','x': -101.25,'y': -87.11,'radius': 0.95},

    # Straight Arterial Avenues
    {'id': 'POTHOLE_13','x': -36.93, 'y': 25.09, 'radius': 0.90},
    {'id': 'POTHOLE_14','x': -42.31, 'y': 15.94, 'radius': 0.95},
    {'id': 'POTHOLE_15','x': -26.43, 'y': -28.33,'radius': 0.90},
    {'id': 'POTHOLE_16','x': -14.11, 'y': -41.02,'radius': 0.95},
    {'id': 'POTHOLE_17','x': 14.94,  'y': -36.93,'radius': 0.90},
    {'id': 'POTHOLE_18','x': 102.31, 'y': 34.69, 'radius': 0.95},
]

def main():
    robot = Supervisor()
    timestep = int(robot.getBasicTimeStep())
    if timestep <= 0:
        timestep = 32

    root_children = robot.getRoot().getField("children")
    print(f"Pothole Swerve & 3D Number Plate Supervisor Online. Monitoring {len(POTHOLES)} potholes.")

    DETECTION_DIST = 18.0
    MAX_SWERVE = 1.8
    SAFETY_GAP = 14.0

    current_offsets = {}
    vehicle_plate_registry = {}

    while robot.step(timestep) != -1:
        n_children = root_children.getCount()
        vehicles = []

        # 1. Discover all active SUMO vehicles and mount 3D Plates
        for i in range(n_children):
            node = root_children.getMFNode(i)
            if node:
                name_field = node.getField("name")
                name = name_field.getSFString() if name_field else ""
                if "SUMO_VEHICLE" in name:
                    t_field = node.getField("translation")
                    r_field = node.getField("rotation")
                    children_field = node.getField("children")

                    # Mount front and rear 3D Number Plates on vehicle spawn
                    if name not in vehicle_plate_registry and children_field:
                        plate_idx = len(vehicle_plate_registry)
                        plate_str = get_unique_indian_plate(plate_idx)
                        vehicle_plate_registry[name] = plate_str

                        # Detect vehicle sub-model
                        v_type = "car"
                        if children_field.getCount() > 0:
                            proto_node = children_field.getMFNode(0)
                            if proto_node:
                                type_name = proto_node.getTypeName().lower()
                                v_type = type_name

                        # Mount Front & Rear 3D Plates
                        front_vrml = create_plate_vrml(plate_str, True, v_type)
                        rear_vrml = create_plate_vrml(plate_str, False, v_type)
                        children_field.importMFNodeFromString(-1, front_vrml)
                        children_field.importMFNodeFromString(-1, rear_vrml)

                    if t_field and r_field:
                        pos = t_field.getSFVec3f()
                        rot = r_field.getSFRotation()
                        vehicles.append({
                            'name': name,
                            't_field': t_field,
                            'pos': pos,
                            'rot': rot,
                        })

        if not vehicles:
            continue

        # 2. Evaluate each vehicle against all potholes
        for v in vehicles:
            name = v['name']
            curr_x, curr_y, curr_z = v['pos']
            rot = v['rot']

            if abs(rot[2]) > 0.5:
                angle = rot[3] if rot[2] > 0 else -rot[3]
            else:
                angle = 0.0

            u_x = math.cos(angle)
            u_y = math.sin(angle)
            n_x = -math.sin(angle)
            n_y = math.cos(angle)

            prior_offset = current_offsets.get(name, 0.0)
            base_x = curr_x - prior_offset * n_x
            base_y = curr_y - prior_offset * n_y

            target_offset = 0.0
            closest_fwd = 999.0

            for pot in POTHOLES:
                px, py = pot['x'], pot['y']
                dx = px - base_x
                dy = py - base_y
                dist = math.hypot(dx, dy)

                if dist < DETECTION_DIST:
                    d_fwd = dx * u_x + dy * u_y
                    d_lat = dx * n_x + dy * n_y

                    if 0.5 < d_fwd < DETECTION_DIST and abs(d_lat) < 2.2:
                        if d_fwd < closest_fwd:
                            closest_fwd = d_fwd
                            swerve_sign = 1.0 if d_lat <= 0.0 else -1.0

                            adjacent_free = True
                            for other in vehicles:
                                if other['name'] == name:
                                    continue
                                ox, oy, _ = other['pos']
                                o_dist = math.hypot(ox - base_x, oy - base_y)

                                if o_dist < SAFETY_GAP:
                                    o_dx = ox - base_x
                                    o_dy = oy - base_y
                                    o_fwd = o_dx * u_x + o_dy * u_y
                                    o_lat = o_dx * n_x + o_dy * n_y

                                    if abs(o_fwd) < 10.0 and (o_lat * swerve_sign) > 0.8:
                                        adjacent_free = False
                                        break

                            if adjacent_free:
                                progress = 1.0 - (d_fwd / DETECTION_DIST)
                                target_offset = swerve_sign * MAX_SWERVE * math.sin(progress * math.pi)
                            else:
                                target_offset = 0.0

            new_offset = prior_offset + (target_offset - prior_offset) * 0.35
            current_offsets[name] = new_offset

            if abs(new_offset) > 0.01:
                final_x = base_x + new_offset * n_x
                final_y = base_y + new_offset * n_y
                v['t_field'].setSFVec3f([final_x, final_y, curr_z])

if __name__ == '__main__':
    main()
