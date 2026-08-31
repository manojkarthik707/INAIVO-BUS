"""
pothole_controller.py — Brown Pothole Avoidance & Dynamic Go-Around Logic.
"""
import math
from controller import Supervisor

POTHOLES = [
    {'id': 'POTHOLE_1', 'x': 161.86, 'y': 187.95, 'radius': 0.85},
    {'id': 'POTHOLE_2', 'x': 185.2, 'y': 190.29, 'radius': 0.9},
    {'id': 'POTHOLE_3', 'x': 182.96, 'y': 186.55, 'radius': 0.85},
    {'id': 'POTHOLE_4', 'x': 162.21, 'y': 184.48, 'radius': 0.9},
    {'id': 'POTHOLE_5', 'x': 73.65, 'y': 223.61, 'radius': 0.85},
    {'id': 'POTHOLE_6', 'x': 96.67, 'y': 232.88, 'radius': 0.9},
    {'id': 'POTHOLE_7', 'x': 159.99, 'y': 240.58, 'radius': 0.85},
    {'id': 'POTHOLE_8', 'x': 203.76, 'y': 227.73, 'radius': 0.9},
    {'id': 'POTHOLE_9', 'x': 228.07, 'y': 163.72, 'radius': 0.85},
    {'id': 'POTHOLE_10', 'x': 220.36, 'y': 109.13, 'radius': 0.9},
    {'id': 'POTHOLE_11', 'x': 141.56, 'y': 74.44, 'radius': 0.85},
    {'id': 'POTHOLE_12', 'x': 73.75, 'y': 100.4, 'radius': 0.9},
    {'id': 'POTHOLE_13', 'x': 138.07, 'y': 212.6, 'radius': 0.85},
    {'id': 'POTHOLE_14', 'x': 132.69, 'y': 203.45, 'radius': 0.9},
    {'id': 'POTHOLE_15', 'x': 148.57, 'y': 159.18, 'radius': 0.85},
    {'id': 'POTHOLE_16', 'x': 160.89, 'y': 146.49, 'radius': 0.9},
    {'id': 'POTHOLE_17', 'x': 189.94, 'y': 150.58, 'radius': 0.85},
    {'id': 'POTHOLE_18', 'x': 277.31, 'y': 222.2, 'radius': 0.9},
]


def main():
    robot = Supervisor()
    timestep = int(robot.getBasicTimeStep())
    if timestep <= 0:
        timestep = 32

    root_children = robot.getRoot().getField("children")
    print(f"Brown Pothole Controller Online. Monitoring {len(POTHOLES)} potholes.")

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
                            # Drive through pothole
                            pass

if __name__ == '__main__':
    main()
