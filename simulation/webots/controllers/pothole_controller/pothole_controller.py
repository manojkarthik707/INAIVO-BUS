"""
pothole_controller.py — Bulletproof Pothole Avoidance & Dynamic Swerve Controller.

Mathematical Principles:
1. Rotation-Derived Unit Heading Vector (u_x, u_y):
   - Computes vehicle forward vector directly from vehicle rotation field.
   - Computes lateral normal vector (n_x, n_y) = (-u_y, u_x) pointing to vehicle's left.
2. Uncorrupted Base Coordinate Tracking:
   - Tracks persistent lateral offset per vehicle to prevent feedback oscillation.
3. Adjacent Lane Free Detection:
   - Evaluates if adjacent lateral space (+/- 14m along track) is unoccupied by other vehicles.
   - If FREE: Smoothly swerves 1.8m into adjacent lane around the pothole.
   - If OCCUPIED: Smoothly drives straight through the crater.
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
    print(f"Pothole Swerve Controller Online. Monitoring {len(POTHOLES)} potholes.")

    DETECTION_DIST = 18.0  # 18m detection window
    MAX_SWERVE = 1.8      # 1.8m lateral swerve width
    SAFETY_GAP = 14.0      # Adjacent lane clearance buffer

    current_offsets = {}

    while robot.step(timestep) != -1:
        n_children = root_children.getCount()
        vehicles = []

        # 1. Gather all active SUMO vehicles
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

            # Extract forward orientation angle from rotation
            if abs(rot[2]) > 0.5:
                angle = rot[3] if rot[2] > 0 else -rot[3]
            else:
                angle = 0.0

            # Forward and lateral unit vectors
            u_x = math.cos(angle)
            u_y = math.sin(angle)
            n_x = -math.sin(angle)
            n_y = math.cos(angle)

            # Retrieve prior lateral offset to deduce base road position
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

                    # Pothole is in front of vehicle (0.5m to 18m ahead, within 2.2m laterally)
                    if 0.5 < d_fwd < DETECTION_DIST and abs(d_lat) < 2.2:
                        if d_fwd < closest_fwd:
                            closest_fwd = d_fwd

                            # Swerve to the left (+n) or right (-n) around pothole
                            swerve_sign = 1.0 if d_lat <= 0.0 else -1.0

                            # Check if adjacent lane is FREE
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

            # Smoothly transition offset
            new_offset = prior_offset + (target_offset - prior_offset) * 0.35
            current_offsets[name] = new_offset

            if abs(new_offset) > 0.01:
                final_x = base_x + new_offset * n_x
                final_y = base_y + new_offset * n_y
                v['t_field'].setSFVec3f([final_x, final_y, curr_z])

if __name__ == '__main__':
    main()
