"""
pothole_controller.py — Flawless Bidirectional Pothole Avoidance with Same-Direction Lane Clearance.

KEY FIXES:
1. Ignores oncoming traffic: Only checks vehicles traveling in the SAME direction (dot_heading > 0.5) when determining if the adjacent lane is free.
2. Full lateral displacement applied directly to vehicle translation: Smooth, visible lane change around potholes.
3. Bidirectional avoidance:
   - When in inner lane (pothole on left/center): Shifts RIGHT into open outer lane.
   - When in outer lane (pothole on right/center): Shifts LEFT into open inner lane.
4. If adjacent lane has a same-direction vehicle alongside: Drives safely straight through without clipping.
"""

import math
from controller import Supervisor

# 18 Terracotta Brown Potholes on Road Centerlines
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
RECOVERY_DIST    = -2.5   # metres past to complete return
TOTAL_SPAN       = DETECTION_DIST - RECOVERY_DIST  # 16.5m
LANE_SHIFT_CAR   = 1.25   # metres shift into adjacent asphalt lane
LANE_SHIFT_BIKE  = 0.85   # metres for 2-wheelers
SMOOTH_RATE      = 0.25   # exponential smoothing per frame
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

    print(f"[PotholeCtrl] Intelligent Pothole Avoidance Supervisor Online ({len(POTHOLES)} potholes).")

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

        # Step 1: Collect active vehicle positions and headings
        active = {}
        for i in range(MAX_VEH):
            vt = veh_trans[i]
            vr = veh_rot[i]
            if vt and vr:
                p = vt.getSFVec3f()
                if p[0] < 9000:
                    h = get_vehicle_heading(vr)
                    active[i] = (p, h)

        # Step 2: Compute smooth lane shift per vehicle
        for i in range(MAX_VEH):
            if i not in active:
                cur_off[i] = 0.0
                continue

            (vx, vy, vz), h = active[i]
            vt = veh_trans[i]

            in_zone = (POT_XMIN <= vx <= POT_XMAX and POT_YMIN <= vy <= POT_YMAX)
            if not in_zone and abs(cur_off[i]) < 0.005:
                cur_off[i] = 0.0
                continue

            ux = math.cos(h)
            uy = math.sin(h)
            nx = -uy   # Left lateral unit vector (+nx = Left, -nx = Right)
            ny = ux

            target_off = 0.0

            if in_zone:
                best_dist  = 999.0
                best_shape = 0.0
                best_dlat  = 0.0

                for (px, py) in POTHOLES:
                    dx = px - vx
                    dy = py - vy

                    d_fwd = dx * ux + dy * uy
                    d_lat = dx * nx + dy * ny

                    # Check if pothole is in this vehicle's travel lane
                    if RECOVERY_DIST <= d_fwd <= DETECTION_DIST and abs(d_lat) < 1.75:
                        if abs(d_fwd) < best_dist:
                            best_dist  = abs(d_fwd)
                            best_dlat  = d_lat
                            progress   = (DETECTION_DIST - d_fwd) / TOTAL_SPAN
                            progress   = max(0.0, min(1.0, progress))
                            best_shape = math.sin(progress * math.pi)

                if best_shape > 0.0:
                    # Determine escape direction:
                    # If pothole is left of car (best_dlat > 0) -> shift RIGHT (-1.0)
                    # If pothole is right of car (best_dlat < 0) -> shift LEFT (+1.0)
                    if best_dlat > 0.05:
                        best_sign = -1.0
                    elif best_dlat < -0.05:
                        best_sign = 1.0
                    else:
                        best_sign = -1.0   # Default shift into open outer lane

                    # Step 3: Adjacent Lane Clearance (SAME DIRECTION VEHICLES ONLY)
                    target_blocked = False
                    for j, ((ox, oy, _), jh) in active.items():
                        if j == i:
                            continue

                        # Check if neighbor is traveling in the SAME direction (ignore oncoming traffic)
                        dot_h = math.cos(h) * math.cos(jh) + math.sin(h) * math.sin(jh)
                        if dot_h < 0.5:
                            continue  # Oncoming vehicle on other side of road -> ignore!

                        odx = ox - vx
                        ody = oy - vy
                        ofwd = odx * ux + ody * uy
                        olat = odx * nx + ody * ny

                        # If same-direction vehicle is alongside us in the target lane
                        if -4.5 <= ofwd <= 7.0 and (olat * best_sign) > 0.70:
                            target_blocked = True
                            break

                    if not target_blocked:
                        shift_mag = LANE_SHIFT_BIKE if veh_is_bike[i] else LANE_SHIFT_CAR
                        target_off = best_sign * shift_mag * best_shape
                    else:
                        # Adjacent lane is occupied by same-direction vehicle -> drive straight
                        target_off = 0.0

            # Step 4: Exponential smoothing
            prev_offset = cur_off[i]
            new_offset  = prev_offset + (target_off - prev_offset) * SMOOTH_RATE

            if abs(new_offset) < 0.003:
                new_offset = 0.0
            cur_off[i] = new_offset

            # Step 5: Apply lateral shift to vehicle translation
            if abs(new_offset) > 0.003:
                vt.setSFVec3f([vx + new_offset * nx, vy + new_offset * ny, vz])


if __name__ == '__main__':
    main()
