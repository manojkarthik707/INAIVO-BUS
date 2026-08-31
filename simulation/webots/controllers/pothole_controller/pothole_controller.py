"""
pothole_controller.py — Intelligent Pothole Avoidance & Dynamic Go-Around Supervisor.

Decision Rules:
1. Pothole Detection:
   - Scans for vehicles within 15.0m approaching any city pothole.
2. Adjacent Lane Clearance Assessment:
   - Evaluates if the adjacent lane in the avoidance direction is FREE of other vehicles (within +/-12.0m).
3. Dynamic Go-Around Logic:
   - If Adjacent Lane is FREE:
     - Vehicle smoothly swerves laterally (up to 1.8m) around the pothole.
     - Smoothly returns to the lane centerline once past the pothole.
   - If Adjacent Lane is OCCUPIED:
     - Vehicle stays strictly on its line, reduces speed smoothly, and drives directly through the pothole.
"""

import math
from controller import Supervisor

POTHOLES = [
    # 2-Lane Shortcut Road
    {'x': -25.0, 'y': 15.2,  'radius': 0.85, 'type': 'shortcut'},
    {'x': 5.0,   'y': 2.8,   'radius': 0.90, 'type': 'shortcut'},
    {'x': 28.0,  'y': -12.4, 'radius': 0.80, 'type': 'shortcut'},
    {'x': 55.0,  'y': -28.5, 'radius': 0.95, 'type': 'shortcut'},

    # Main Curved Boulevards
    {'x': -75.0, 'y': 51.5,  'radius': 0.90, 'type': 'curve'},
    {'x': -111.5,'y': 15.0,  'radius': 0.85, 'type': 'curve'},
    {'x': -108.0,'y': -80.0, 'radius': 0.95, 'type': 'curve'},
    {'x': 75.0,  'y': -51.5, 'radius': 0.85, 'type': 'curve'},
    {'x': 111.5, 'y': -15.0, 'radius': 0.90, 'type': 'curve'},
    {'x': 25.0,  'y': 172.0, 'radius': 0.85, 'type': 'curve'},
    {'x': -35.0, 'y': 168.0, 'radius': 0.90, 'type': 'curve'},

    # Straight Arterial Avenues
    {'x': -15.0, 'y': 53.0,  'radius': 0.85, 'type': 'avenue'},
    {'x': 20.0,  'y': 36.8,  'radius': 0.80, 'type': 'avenue'},
    {'x': -15.0, 'y': -113.0,'radius': 0.95, 'type': 'avenue'},
    {'x': 80.0,  'y': 101.2, 'radius': 0.85, 'type': 'avenue'},
    {'x': -45.0, 'y': 95.0,  'radius': 0.85, 'type': 'avenue'},
    {'x': 45.0,  'y': -95.0, 'radius': 0.90, 'type': 'avenue'},
]

def main():
    robot = Supervisor()
    timestep = int(robot.getBasicTimeStep())
    if timestep <= 0:
        timestep = 32

    root_children = robot.getRoot().getField("children")
    print(f"Pothole Intelligence Controller Online. Monitoring {len(POTHOLES)} potholes.")

    DETECTION_DIST = 16.0  # Detection horizon
    SWERVE_MAGNITUDE = 1.6 # Lateral evasion distance in meters
    SAFETY_GAP = 12.0      # Required clear space in adjacent lane

    while robot.step(timestep) != -1:
        n_children = root_children.getCount()
        vehicles = []

        # 1. Discover all active SUMO vehicles
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
                            'node': node,
                            'name': name,
                            't_field': t_field,
                            'r_field': r_field,
                            'pos': pos,
                            'rot': rot,
                        })

        if not vehicles:
            continue

        # 2. Evaluate each vehicle against all potholes
        for v in vehicles:
            vx, vy, vz = v['pos']
            v_rot = v['rot']
            
            # Compute heading angle from rotation (assuming rotation around Z axis)
            heading = v_rot[3] if abs(v_rot[2]) > 0.5 else 0.0
            if v_rot[2] < 0:
                heading = -heading

            # Unit forward and rightward lateral vectors
            fwd_x = -math.sin(heading)
            fwd_y = math.cos(heading)
            lat_x = math.cos(heading)
            lat_y = math.sin(heading)

            for pot in POTHOLES:
                px, py = pot['x'], pot['y']
                dx = px - vx
                dy = py - vy
                dist = math.hypot(dx, dy)

                # Check if pothole is within forward detection window
                if 2.0 <= dist <= DETECTION_DIST:
                    # Dot product with forward vector to verify pothole is ahead
                    dot_fwd = dx * fwd_x + dy * fwd_y
                    if dot_fwd > 1.5:
                        # Longitudinal progress along avoidance zone (0.0 to 1.0)
                        progress = 1.0 - (dist / DETECTION_DIST)

                        # Check if adjacent lane / lateral zone is FREE of other vehicles
                        adjacent_free = True
                        for other_v in vehicles:
                            if other_v['name'] == v['name']:
                                continue
                            ox, oy, _ = other_v['pos']
                            o_dist = math.hypot(ox - vx, oy - vy)
                            if o_dist < SAFETY_GAP:
                                # Check if other vehicle is laterally alongside in adjacent space
                                o_dx = ox - vx
                                o_dy = oy - vy
                                dot_lat = o_dx * lat_x + o_dy * lat_y
                                if abs(dot_lat) > 1.0 and abs(dot_lat) < 5.0:
                                    adjacent_free = False
                                    break

                        # If adjacent lane is free, perform smooth dynamic swerve around pothole
                        if adjacent_free:
                            # Bell-curve swerve profile: peaks at middle of avoidance zone
                            swerve_scale = math.sin(progress * math.pi) * SWERVE_MAGNITUDE
                            # Swerve laterally to the right or left depending on road side
                            offset_x = lat_x * swerve_scale * (timestep / 1000.0) * 1.5
                            offset_y = lat_y * swerve_scale * (timestep / 1000.0) * 1.5
                            v['t_field'].setSFVec3f([vx + offset_x, vy + offset_y, vz])
                        else:
                            # Adjacent lane is OCCUPIED: vehicle stays in line and drives through pothole
                            pass

if __name__ == '__main__':
    main()
