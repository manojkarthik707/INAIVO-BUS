"""
pothole_controller.py — Dynamic Pothole Swerve Supervisor.

Uses velocity-tracked heading to apply sinusoidal lateral offsets around potholes.
Adjacent lane clearance check: 
  - Free -> swerve 1.8m around pothole
  - Occupied -> drive straight through
"""

import math
from controller import Supervisor

POTHOLES = [
    {'id': 'POTHOLE_1',  'x': -13.14, 'y':  0.44},
    {'id': 'POTHOLE_2',  'x':  10.20, 'y':  2.78},
    {'id': 'POTHOLE_3',  'x':   7.96, 'y': -0.96},
    {'id': 'POTHOLE_4',  'x': -12.79, 'y': -3.03},
    {'id': 'POTHOLE_5',  'x': -101.35,'y': 36.10},
    {'id': 'POTHOLE_6',  'x': -78.33, 'y': 45.37},
    {'id': 'POTHOLE_7',  'x': -15.01, 'y': 53.07},
    {'id': 'POTHOLE_8',  'x':  28.76, 'y': 40.22},
    {'id': 'POTHOLE_9',  'x':  53.07, 'y': -23.79},
    {'id': 'POTHOLE_10', 'x':  45.36, 'y': -78.38},
    {'id': 'POTHOLE_11', 'x': -33.44, 'y': -113.07},
    {'id': 'POTHOLE_12', 'x': -101.25,'y': -87.11},
    {'id': 'POTHOLE_13', 'x': -36.93, 'y':  25.09},
    {'id': 'POTHOLE_14', 'x': -42.31, 'y':  15.94},
    {'id': 'POTHOLE_15', 'x': -26.43, 'y': -28.33},
    {'id': 'POTHOLE_16', 'x': -14.11, 'y': -41.02},
    {'id': 'POTHOLE_17', 'x':  14.94, 'y': -36.93},
    {'id': 'POTHOLE_18', 'x':  102.31,'y':  34.69},
]

DETECTION_DIST = 16.0
MAX_SWERVE     = 1.7
SAFETY_GAP     = 12.0
SMOOTH_RATE    = 0.30

def main():
    robot = Supervisor()
    timestep = int(robot.getBasicTimeStep())
    if timestep <= 0:
        timestep = 32

    root_children = robot.getRoot().getField("children")
    print(f"Pothole Swerve Supervisor Online. Monitoring {len(POTHOLES)} potholes.")

    prev_pos   = {}   # name -> (px, py)
    cur_offset = {}   # name -> current lateral offset (m)

    while robot.step(timestep) != -1:
        n = root_children.getCount()
        vehicles = []

        for i in range(n):
            node = root_children.getMFNode(i)
            if not node:
                continue
            nf = node.getField("name")
            if not nf:
                continue
            name = nf.getSFString()
            if "SUMO_VEHICLE" not in name:
                continue
            tf = node.getField("translation")
            if not tf:
                continue
            pos = tf.getSFVec3f()
            if pos[0] > 9000:
                continue
            vehicles.append({'name': name, 'tf': tf, 'pos': pos})

        if not vehicles:
            continue

        for v in vehicles:
            name = v['name']
            cx, cy, cz = v['pos']

            # Compute motion heading from displacement
            if name in prev_pos:
                ox, oy = prev_pos[name]
                ddx, ddy = cx - ox, cy - oy
                d = math.hypot(ddx, ddy)
                if d > 0.005:
                    ux, uy = ddx / d, ddy / d
                else:
                    ux, uy = 1.0, 0.0
            else:
                ux, uy = 1.0, 0.0
            prev_pos[name] = (cx, cy)

            # Lateral normal (left of forward)
            nx, ny = -uy, ux

            # Strip current lateral offset to find base road position
            off = cur_offset.get(name, 0.0)
            bx = cx - off * nx
            by = cy - off * ny

            target_off = 0.0
            best_fwd   = 999.0

            for pot in POTHOLES:
                dx = pot['x'] - bx
                dy = pot['y'] - by
                dist = math.hypot(dx, dy)
                if dist >= DETECTION_DIST:
                    continue

                d_fwd = dx * ux + dy * uy
                d_lat = dx * nx + dy * ny

                if 0.8 < d_fwd < DETECTION_DIST and abs(d_lat) < 2.0:
                    if d_fwd < best_fwd:
                        best_fwd = d_fwd
                        sign = 1.0 if d_lat <= 0.0 else -1.0

                        # Check adjacent lane clearance
                        clear = True
                        for ov in vehicles:
                            if ov['name'] == name:
                                continue
                            ox2, oy2, _ = ov['pos']
                            od = math.hypot(ox2 - bx, oy2 - by)
                            if od < SAFETY_GAP:
                                ofwd = (ox2 - bx) * ux + (oy2 - by) * uy
                                olat = (ox2 - bx) * nx + (oy2 - by) * ny
                                if abs(ofwd) < 9.0 and olat * sign > 0.7:
                                    clear = False
                                    break

                        if clear:
                            progress = 1.0 - d_fwd / DETECTION_DIST
                            target_off = sign * MAX_SWERVE * math.sin(progress * math.pi)
                        else:
                            target_off = 0.0

            # Smooth lerp towards target
            new_off = off + (target_off - off) * SMOOTH_RATE
            cur_offset[name] = new_off

            if abs(new_off) > 0.02:
                v['tf'].setSFVec3f([bx + new_off * nx, by + new_off * ny, cz])

if __name__ == '__main__':
    main()
