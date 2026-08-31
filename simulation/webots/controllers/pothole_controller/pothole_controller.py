"""
pothole_controller.py — Precision Dynamic Vehicle Pothole Avoidance & Swerve Controller.

Architecture:
1. Webots Vehicle Local Coordinate System:
   - Child node translation Y-axis is strictly LATERAL (left/right).
   - Manipulating child PROTO translation avoids SumoInterface root translation overwrite.
2. Distance & Lateral Evasion:
   - Detection Window: 18.0m upstream of pothole.
   - Adjacent Lane Scanning: Evaluates if adjacent lane in swerve direction has no vehicles within 14.0m.
   - If FREE: Executes a smooth 1.8m sinusoidal swerve around the pothole into the adjacent free space, then smoothly returns to 0.0m once past.
   - If OCCUPIED: Remains centered at 0.0m offset and drives directly through the pothole.
"""

import math
from controller import Supervisor

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
    print(f"Pothole Swerve Supervisor Online. Active potholes: {len(POTHOLES)}")

    DETECTION_DIST = 18.0  # Detection horizon
    MAX_SWERVE = 1.8      # Maximum lateral swerve in meters
    SAFETY_GAP = 14.0      # Adjacent lane clearance buffer

    vehicle_defaults = {}

    while robot.step(timestep) != -1:
        n_children = root_children.getCount()
        active_vehicles = []

        for i in range(n_children):
            node = root_children.getMFNode(i)
            if node:
                name_field = node.getField("name")
                name = name_field.getSFString() if name_field else ""
                if "SUMO_VEHICLE" in name:
                    t_field = node.getField("translation")
                    r_field = node.getField("rotation")
                    children_field = node.getField("children")

                    if t_field and r_field and children_field and children_field.getCount() > 0:
                        child_node = children_field.getMFNode(0)
                        child_t_field = child_node.getField("translation") if child_node else None

                        if child_t_field:
                            if name not in vehicle_defaults:
                                vehicle_defaults[name] = child_t_field.getSFVec3f()

                            pos = t_field.getSFVec3f()
                            rot = r_field.getSFRotation()
                            active_vehicles.append({
                                'name': name,
                                'pos': pos,
                                'rot': rot,
                                'child_t_field': child_t_field,
                                'def_t': vehicle_defaults[name],
                            })

        if not active_vehicles:
            continue

        for v in active_vehicles:
            vx, vy, vz = v['pos']
            v_rot = v['rot']

            angle = v_rot[3] if abs(v_rot[2]) > 0.5 else 0.0
            if v_rot[2] < 0:
                angle = -angle

            fwd_x = -math.sin(angle)
            fwd_y = math.cos(angle)
            lat_x = math.cos(angle)
            lat_y = math.sin(angle)

            target_lateral_offset = 0.0
            closest_pothole_dist = 999.0

            for pot in POTHOLES:
                px, py = pot['x'], pot['y']
                dx = px - vx
                dy = py - vy
                dist = math.hypot(dx, dy)

                if dist < DETECTION_DIST:
                    dist_fwd = dx * fwd_x + dy * fwd_y
                    dist_lat = dx * lat_x + dy * lat_y

                    if 0.5 < dist_fwd < DETECTION_DIST and abs(dist_lat) < 2.2:
                        if dist_fwd < closest_pothole_dist:
                            closest_pothole_dist = dist_fwd

                            swerve_sign = 1.0 if dist_lat <= 0.2 else -1.0

                            adjacent_free = True
                            for other in active_vehicles:
                                if other['name'] == v['name']:
                                    continue
                                ox, oy, _ = other['pos']
                                o_dist = math.hypot(ox - vx, oy - vy)

                                if o_dist < SAFETY_GAP:
                                    o_dx = ox - vx
                                    o_dy = oy - vy
                                    o_lat = o_dx * lat_x + o_dy * lat_y
                                    o_fwd = o_dx * fwd_x + o_dy * fwd_y

                                    if abs(o_fwd) < 10.0 and (o_lat * swerve_sign) > 1.0:
                                        adjacent_free = False
                                        break

                            if adjacent_free:
                                progress = 1.0 - (dist_fwd / DETECTION_DIST)
                                target_lateral_offset = swerve_sign * MAX_SWERVE * math.sin(progress * math.pi)
                            else:
                                target_lateral_offset = 0.0

            def_x, def_y, def_z = v['def_t']
            current_child_t = v['child_t_field'].getSFVec3f()
            current_lat = current_child_t[1] - def_y

            new_lat = current_lat + (target_lateral_offset - current_lat) * 0.25
            v['child_t_field'].setSFVec3f([def_x, def_y + new_lat, def_z])

if __name__ == '__main__':
    main()
