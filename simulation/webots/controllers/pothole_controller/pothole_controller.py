"""
pothole_controller.py — Optimized Dynamic Pothole Swerve Supervisor.

Performance:
  - Vehicle field refs cached at startup (no getField in loop).
  - Full N²-neighbour check only every 3 steps.
  - Skips vehicles further than DETECTION_DIST from any pothole via bounding box fast-reject.
"""

import math
from controller import Supervisor

POTHOLES = [
    (-13.14,   0.44), ( 10.20,   2.78), (  7.96,  -0.96), (-12.79,  -3.03),
    (-101.35, 36.10), (-78.33,  45.37), (-15.01,  53.07), ( 28.76,  40.22),
    ( 53.07, -23.79), ( 45.36, -78.38), (-33.44,-113.07), (-101.25,-87.11),
    (-36.93,  25.09), (-42.31,  15.94), (-26.43, -28.33), (-14.11, -41.02),
    ( 14.94, -36.93), (102.31,  34.69),
]

# Precompute bounding box for fast reject
_px = [p[0] for p in POTHOLES]
_py = [p[1] for p in POTHOLES]
POT_XMIN = min(_px) - 20
POT_XMAX = max(_px) + 20
POT_YMIN = min(_py) - 20
POT_YMAX = max(_py) + 20

DETECTION_DIST = 16.0
MAX_SWERVE     = 1.7
SAFETY_GAP     = 12.0
SMOOTH_RATE    = 0.30
MAX_VEH        = 100
UPDATE_EVERY   = 3   # run pothole logic every N steps


def main():
    robot    = Supervisor()
    timestep = int(robot.getBasicTimeStep()) or 32
    root_ch  = robot.getRoot().getField("children")

    print(f"[PotholeCtrl] Monitoring {len(POTHOLES)} potholes. Caching vehicle refs...")

    # Cache vehicle field refs by DEF name — resolve lazily
    veh_trans = [None] * MAX_VEH

    def resolve_vehicles():
        for i in range(MAX_VEH):
            if veh_trans[i] is None:
                node = robot.getFromDef(f"SUMO_VEHICLE{i}")
                if node:
                    veh_trans[i] = node.getField("translation")

    resolve_vehicles()
    print(f"[PotholeCtrl] {sum(1 for t in veh_trans if t)} vehicle refs resolved. Running.")

    prev_pos   = {}   # index -> (px, py)
    cur_offset = {}   # index -> current lateral offset

    step = 0
    while robot.step(timestep) != -1:
        step += 1

        if step % 60 == 0:
            resolve_vehicles()

        if step % UPDATE_EVERY != 0:
            continue

        # Collect active vehicle positions
        active = []   # list of (index, x, y, tf)
        for i in range(MAX_VEH):
            tf = veh_trans[i]
            if not tf:
                continue
            pos = tf.getSFVec3f()
            vx, vy, vz = pos
            if vx > 9000:
                continue
            # Fast bounding-box reject — skip if nowhere near any pothole
            if vx < POT_XMIN or vx > POT_XMAX or vy < POT_YMIN or vy > POT_YMAX:
                continue
            active.append((i, vx, vy, vz, tf))

        if not active:
            continue

        for idx, cx, cy, cz, tf in active:
            # Compute heading from displacement
            if idx in prev_pos:
                ox, oy = prev_pos[idx]
                ddx, ddy = cx - ox, cy - oy
                d = math.hypot(ddx, ddy)
                ux, uy = (ddx/d, ddy/d) if d > 0.005 else (1.0, 0.0)
            else:
                ux, uy = 1.0, 0.0
            prev_pos[idx] = (cx, cy)

            # Lateral normal (left of forward)
            nx, ny = -uy, ux

            # Strip current offset to find base road position
            off = cur_offset.get(idx, 0.0)
            bx  = cx - off * nx
            by  = cy - off * ny

            target_off = 0.0
            best_fwd   = 999.0

            for (px, py) in POTHOLES:
                dx = px - bx
                dy = py - by
                dist = math.hypot(dx, dy)
                if dist >= DETECTION_DIST:
                    continue

                d_fwd = dx * ux + dy * uy
                d_lat = dx * nx + dy * ny

                if 0.8 < d_fwd < DETECTION_DIST and abs(d_lat) < 2.0:
                    if d_fwd < best_fwd:
                        best_fwd = d_fwd
                        sign = 1.0 if d_lat <= 0.0 else -1.0

                        # Check adjacent lane clearance (only vs nearby vehicles)
                        clear = True
                        for jdx, ox2, oy2, _, _ in active:
                            if jdx == idx:
                                continue
                            if math.hypot(ox2 - bx, oy2 - by) >= SAFETY_GAP:
                                continue
                            ofwd = (ox2 - bx)*ux + (oy2 - by)*uy
                            olat = (ox2 - bx)*nx + (oy2 - by)*ny
                            if abs(ofwd) < 9.0 and olat * sign > 0.7:
                                clear = False
                                break

                        if clear:
                            progress = 1.0 - d_fwd / DETECTION_DIST
                            target_off = sign * MAX_SWERVE * math.sin(progress * math.pi)
                        else:
                            target_off = 0.0

            new_off = off + (target_off - off) * SMOOTH_RATE
            cur_offset[idx] = new_off

            if abs(new_off) > 0.02:
                tf.setSFVec3f([bx + new_off * nx, by + new_off * ny, cz])


if __name__ == '__main__':
    main()
