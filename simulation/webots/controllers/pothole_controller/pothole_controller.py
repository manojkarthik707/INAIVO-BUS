"""
pothole_controller.py — Strict On-Road Pothole Avoidance via Adjacent Lane Shift.

RULES:
1. NEVER swerve towards the curb / sand (negative offset).
2. Potholes are in Lane 0 (outer lane); the only escape is shifting LEFT (+nx) into Lane 1 (adjacent asphalt driving lane).
3. If Lane 1 has a vehicle alongside (-6m to +9m, olat > 0.6m): DO NOT SWERVE. Drive straight through.
4. If Lane 1 is clear: Smoothly shift left onto the adjacent asphalt lane (1.40m), clear the pothole, and return.
"""

import math
from controller import Supervisor

# 18 Terracotta Brown Potholes on Road Centerlines (all in Lane 0)
POTHOLES = [
    (-13.14,   0.44), ( 10.20,   2.78), (  7.96,  -0.96), (-12.79,  -3.03),
    (-101.35, 36.10), (-78.33,  45.37), (-15.01,  53.07), ( 28.76,  40.22),
    ( 53.07, -23.79), ( 45.36, -78.38), (-33.44,-113.07), (-101.25,-87.11),
    (-36.93,  25.09), (-42.31,  15.94), (-26.43, -28.33), (-14.11, -41.02),
    ( 14.94, -36.93), (102.31,  34.69),
]

_px = [p[0] for p in POTHOLES]
_py = [p[1] for p in POTHOLES]
POT_XMIN = min(_px) - 30.0
POT_XMAX = max(_px) + 30.0
POT_YMIN = min(_py) - 30.0
POT_YMAX = max(_py) + 30.0

DETECTION_DIST   = 14.0   # metres ahead to begin lane shift
RECOVERY_DIST    = -2.5   # metres past to complete return to lane
TOTAL_SPAN       = DETECTION_DIST - RECOVERY_DIST  # 16.5m
LANE_SHIFT_CAR   = 1.35   # metres LEFT into Lane 1 (pure asphalt, stays on road)
LANE_SHIFT_BIKE  = 0.85   # metres for 2-wheelers
SMOOTH_RATE      = 0.20   # exponential smoothing per 32ms frame
MAX_VEH          = 100


def get_vehicle_heading(vr):
    """Extract true car-front heading from rotation field."""
    rot = vr.getSFRotation()
    ax, ay, az, angle = rot
    if az > 0.5:
        yaw = angle
    elif az < -0.5:
        yaw = -angle
    else:
        yaw = 0.0
    return -yaw


def main():
    robot    = Supervisor()
    timestep = int(robot.getBasicTimeStep()) or 32

    print(f"[PotholeCtrl] In-Road Lane-Shift Supervisor Online ({len(POTHOLES)} potholes).")

    veh_trans   = [None] * MAX_VEH
    veh_rot     = [None] * MAX_VEH
    veh_is_bike = [False] * MAX_VEH
    cur_off     = [0.0]  * MAX_VEH

    def resolve_vehicles():
        for i in range(MAX_VEH):
            if veh_trans[i] is None:
                node = robot.getFromDef(f"SUMO_VEHICLE{i}")
                if node:
                    veh_trans[i] = node.getField("translation")
                    veh_rot[i]   = node.getField("rotation")
                    ch_f = node.getField("children")
                    if ch_f and ch_f.getCount() > 0:
                        proto = ch_f.getMFNode(0)
                        if proto:
                            tname = proto.getTypeName().lower()
                            if "motor" in tname or "scoot" in tname or "bike" in tname:
                                veh_is_bike[i] = True

    resolve_vehicles()
    print(f"[PotholeCtrl] {sum(1 for t in veh_trans if t)} vehicle refs cached.")

    step = 0
    while robot.step(timestep) != -1:
        step += 1

        if step % 90 == 0:
            resolve_vehicles()

        # Step 1: Collect active vehicle positions
        active_positions = {}
        for i in range(MAX_VEH):
            vt = veh_trans[i]
            if vt:
                p = vt.getSFVec3f()
                if p[0] < 9000:
                    active_positions[i] = p

        # Step 2: Process each vehicle
        for i in range(MAX_VEH):
            if i not in active_positions:
                cur_off[i] = 0.0
                continue

            vt = veh_trans[i]
            vr = veh_rot[i]
            if not vr:
                continue

            vx, vy, vz = active_positions[i]

            in_zone = (POT_XMIN <= vx <= POT_XMAX and POT_YMIN <= vy <= POT_YMAX)
            if not in_zone and abs(cur_off[i]) < 0.005:
                continue

            h = get_vehicle_heading(vr)
            ux = math.cos(h)
            uy = math.sin(h)
            nx = -uy   # Lateral unit vector pointing strictly LEFT (towards Lane 1 / road center)
            ny = ux

            target_off = 0.0

            if in_zone:
                best_dist  = 999.0
                best_shape = 0.0

                for (px, py) in POTHOLES:
                    dx = px - vx
                    dy = py - vy

                    d_fwd = dx * ux + dy * uy
                    d_lat = dx * nx + dy * ny

                    # Check if pothole is directly in front of this vehicle
                    if RECOVERY_DIST <= d_fwd <= DETECTION_DIST and abs(d_lat) < 1.70:
                        if abs(d_fwd) < best_dist:
                            best_dist = abs(d_fwd)
                            progress = (DETECTION_DIST - d_fwd) / TOTAL_SPAN
                            progress = max(0.0, min(1.0, progress))
                            best_shape = math.sin(progress * math.pi)

                if best_shape > 0.0:
                    # Step 3: Adjacent Lane Vehicle Clearance Check
                    # Check if any vehicle is currently in Lane 1 beside or near us
                    lane_1_clear = True
                    for j, (ox, oy, _) in active_positions.items():
                        if j == i:
                            continue
                        odx = ox - vx
                        ody = oy - vy
                        ofwd = odx * ux + ody * uy
                        olat = odx * nx + ody * ny

                        # If neighbor is in Lane 1 (olat between 0.6m and 3.5m) alongside us (-6m to +9m)
                        if -6.0 <= ofwd <= 9.0 and 0.6 <= olat <= 3.5:
                            lane_1_clear = False
                            break

                    if lane_1_clear:
                        # Shift LEFT (+nx) into adjacent asphalt Lane 1 (NEVER to the right/curb)
                        shift_mag = LANE_SHIFT_BIKE if veh_is_bike[i] else LANE_SHIFT_CAR
                        target_off = +1.0 * shift_mag * best_shape
                    else:
                        # Lane 1 is occupied -> DO NOT SWERVE, stay straight on road through pothole
                        target_off = 0.0

            # Step 4: Exponential smoothing for smooth lane shift
            prev_offset = cur_off[i]
            new_offset  = prev_offset + (target_off - prev_offset) * SMOOTH_RATE

            if abs(new_offset) < 0.002:
                new_offset = 0.0
            cur_off[i] = new_offset

            if abs(new_offset) > 0.002:
                vt.setSFVec3f([vx + new_offset * nx, vy + new_offset * ny, vz])


if __name__ == '__main__':
    main()
