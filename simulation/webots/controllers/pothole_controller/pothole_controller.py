"""
pothole_controller.py — Motion-Vector Powered Dynamic Pothole Avoidance Controller.

Robust Velocity-Vector Mathematics:
1. Calculates instantaneous motion vector (u_x, u_y) from vehicle displacement.
2. Calculates exact perpendicular lateral normal vector (n_x, n_y) = (-u_y, u_x).
3. Evaluates forward distance and lateral offset to all 18 potholes.
4. If pothole is directly ahead in vehicle path (0.5m < d_fwd < 16.0m, |d_lat| < 1.8m):
   - Scans adjacent lane for other vehicles within 12.0m.
   - If Adjacent Lane is FREE:
     - Applies a smooth 1.7m lateral sinusoidal swerve perpendicular to vehicle trajectory.
   - If Adjacent Lane is OCCUPIED:
     - Holds trajectory and drives straight through.
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
    print(f"Motion-Vector Pothole Swerve Controller Online. Monitoring {len(POTHOLES)} potholes.")

    DETECTION_DIST = 16.0  # 16m detection horizon
    SWERVE_AMOUNT = 1.7   # 1.7m lateral swerve (fits perfectly within adjacent 3.5m lane)
    SAFETY_GAP = 12.0     # Required clear buffer in adjacent lane

    # Track previous position to compute true motion vector
    prev_positions = {}

    while robot.step(timestep) != -1:
        n_children = root_children.getCount()
        vehicles = []

        # 1. Discover all active vehicles
        for i in range(n_children):
            node = root_children.getMFNode(i)
            if node:
                name_field = node.getField("name")
                name = name_field.getSFString() if name_field else ""
                if "SUMO_VEHICLE" in name:
                    t_field = node.getField("translation")
                    if t_field:
                        pos = t_field.getSFVec3f()
                        vehicles.append({
                            'name': name,
                            'node': node,
                            't_field': t_field,
                            'x': pos[0],
                            'y': pos[1],
                            'z': pos[2],
                        })

        if not vehicles:
            continue

        # 2. Process each vehicle
        for v in vehicles:
            name = v['name']
            vx, vy, vz = v['x'], v['y'], v['z']

            # Compute motion vector from previous position
            if name in prev_positions:
                px_prev, py_prev = prev_positions[name]
                dx_move = vx - px_prev
                dy_move = vy - py_prev
                move_dist = math.hypot(dx_move, dy_move)
                if move_dist > 0.01:
                    u_x = dx_move / move_dist
                    u_y = dy_move / move_dist
                else:
                    u_x, u_y = 1.0, 0.0
            else:
                u_x, u_y = 1.0, 0.0

            # Store current position for next step
            prev_positions[name] = (vx, vy)

            # Perpendicular lateral normal vector (pointing to vehicle's left)
            n_x = -u_y
            n_y = u_x

            # Find closest approaching pothole
            closest_dist_fwd = 999.0
            chosen_swerve = 0.0

            for pot in POTHOLES:
                px, py = pot['x'], pot['y']
                dx = px - vx
                dy = py - vy
                dist = math.hypot(dx, dy)

                if dist < DETECTION_DIST:
                    # Forward distance along vehicle motion vector
                    d_fwd = dx * u_x + dy * u_y
                    # Lateral offset relative to vehicle path
                    d_lat = dx * n_x + dy * n_y

                    # If pothole is directly in front of the vehicle (0.5m to 16.0m ahead, |d_lat| < 1.8m)
                    if 0.5 < d_fwd < DETECTION_DIST and abs(d_lat) < 1.8:
                        if d_fwd < closest_dist_fwd:
                            closest_dist_fwd = d_fwd

                            # Swerve away from the pothole center:
                            # If pothole is to vehicle's right (d_lat <= 0), swerve left (+n); if to left (d_lat > 0), swerve right (-n)
                            swerve_dir = 1.0 if d_lat <= 0.0 else -1.0

                            # Check if adjacent lane space in swerve direction is FREE
                            adjacent_free = True
                            for other in vehicles:
                                if other['name'] == name:
                                    continue
                                ox, oy = other['x'], other['y']
                                o_dist = math.hypot(ox - vx, oy - vy)

                                if o_dist < SAFETY_GAP:
                                    o_dx = ox - vx
                                    o_dy = oy - vy
                                    o_fwd = o_dx * u_x + o_dy * u_y
                                    o_lat = o_dx * n_x + o_dy * n_y

                                    # Check if other vehicle is occupying adjacent space in swerve direction
                                    if abs(o_fwd) < 9.0 and (o_lat * swerve_dir) > 0.8:
                                        adjacent_free = False
                                        break

                            if adjacent_free:
                                # Smooth sinusoidal bell-curve swerve peak at middle of avoidance zone
                                progress = 1.0 - (d_fwd / DETECTION_DIST)
                                swerve_scale = math.sin(progress * math.pi)
                                chosen_swerve = swerve_dir * SWERVE_AMOUNT * swerve_scale
                            else:
                                # Adjacent lane occupied -> drive straight through
                                chosen_swerve = 0.0

            # Apply smooth lateral shift directly to vehicle position
            if abs(chosen_swerve) > 0.01:
                new_vx = vx + chosen_swerve * n_x
                new_vy = vy + chosen_swerve * n_y
                v['t_field'].setSFVec3f([new_vx, new_vy, vz])

if __name__ == '__main__':
    main()
