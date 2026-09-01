"""
pothole_controller.py — Bidirectional Intelligent Pothole Avoidance (Adjacent Lane Shift).

RULES:
1. Bidirectional avoidance:
   - If pothole is on left (or vehicle is in inner lane): Swerve RIGHT into open outer lane.
   - If pothole is on right (or vehicle is in outer lane): Swerve LEFT into open inner lane.
2. Dynamic adjacent lane clearance:
   - Checks if any neighbor vehicle is driving alongside on the target swerve side.
   - If the adjacent lane is OCCUPIED: DO NOT SWERVE (stay straight, drive safely through pothole).
   - If the adjacent lane is FREE: Smoothly shift onto the free asphalt lane, clear the pothole, and return.
3. Zero world-coordinate accumulation: Uses local-frame PROTO translation [0, offset, 0].
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

DETECTION_DIST   = 13.0   # metres ahead to begin lane shift
RECOVERY_DIST    = -2.0   # metres past to complete return
TOTAL_SPAN       = DETECTION_DIST - RECOVERY_DIST  # 15.0m
LANE_SHIFT_CAR   = 1.05   # metres shift into adjacent asphalt lane
LANE_SHIFT_BIKE  = 0.70   # metres for 2-wheelers
SMOOTH_RATE      = 0.22   # exponential smoothing per frame
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

    print(f"[PotholeCtrl] Bidirectional Lane-Shift Supervisor Online ({len(POTHOLES)} potholes).")

    veh_trans   = [None] * MAX_VEH   # Solid world translation (read-only)
    veh_rot     = [None] * MAX_VEH   # Solid world rotation (read-only)
    proto_trans = [None] * MAX_VEH   # Child PROTO local translation field [0, Y, 0]
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
                            proto_trans[i] = proto.getField("translation")
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

        # Step 1: Collect world positions for neighbor clearance checks
        active_positions = {}
        for i in range(MAX_VEH):
            vt = veh_trans[i]
            if vt:
                p = vt.getSFVec3f()
                if p[0] < 9000:
                    active_positions[i] = p

        # Step 2: Compute smooth local lateral offset per vehicle
        for i in range(MAX_VEH):
            if i not in active_positions:
                cur_off[i] = 0.0
                continue

            vr = veh_rot[i]
            pt = proto_trans[i]
            if not vr:
                continue

            vx, vy, vz = active_positions[i]

            in_zone = (POT_XMIN <= vx <= POT_XMAX and POT_YMIN <= vy <= POT_YMAX)
            if not in_zone and abs(cur_off[i]) < 0.005:
                if pt and abs(cur_off[i]) > 0.001:
                    pt.setSFVec3f([0.0, 0.0, 0.0])
                    cur_off[i] = 0.0
                continue

            h = get_vehicle_heading(vr)
            ux = math.cos(h)
            uy = math.sin(h)
            nx = -uy   # Left lateral unit vector in world XY (+nx = Left, -nx = Right)
            ny = ux

            target_off = 0.0
            best_sign  = 0.0

            if in_zone:
                best_dist  = 999.0
                best_shape = 0.0
                best_dlat  = 0.0

                for (px, py) in POTHOLES:
                    dx = px - vx
                    dy = py - vy

                    d_fwd = dx * ux + dy * uy
                    d_lat = dx * nx + dy * ny

                    # Check if pothole is directly in this vehicle's track
                    if RECOVERY_DIST <= d_fwd <= DETECTION_DIST and abs(d_lat) < 1.75:
                        if abs(d_fwd) < best_dist:
                            best_dist  = abs(d_fwd)
                            best_dlat  = d_lat
                            progress   = (DETECTION_DIST - d_fwd) / TOTAL_SPAN
                            progress   = max(0.0, min(1.0, progress))
                            best_shape = math.sin(progress * math.pi)

                if best_shape > 0.0:
                    # Determine safest avoidance direction:
                    # If pothole is to the vehicle's left (d_lat > 0.1) -> swerve RIGHT (-1.0) into outer lane
                    # If pothole is to the vehicle's right (d_lat < -0.1) -> swerve LEFT (+1.0) into inner lane
                    # If centered: default away from center line
                    if best_dlat > 0.05:
                        best_sign = -1.0  # Swerve RIGHT
                    elif best_dlat < -0.05:
                        best_sign = 1.0   # Swerve LEFT
                    else:
                        best_sign = -1.0  # Default rightward shift into open lane

                    # Step 3: Adjacent Lane Clearance Check
                    # Check if any neighbor vehicle is in the target lane alongside us
                    target_lane_blocked = False
                    for j, (ox, oy, _) in active_positions.items():
                        if j == i:
                            continue
                        odx = ox - vx
                        ody = oy - vy
                        ofwd = odx * ux + ody * uy
                        olat = odx * nx + ody * ny

                        # If neighbor is alongside us (-5m to +8m) on the side we want to steer towards
                        if -5.0 <= ofwd <= 8.0 and (olat * best_sign) > 0.45:
                            target_lane_blocked = True
                            break

                    if not target_lane_blocked:
                        shift_mag = LANE_SHIFT_BIKE if veh_is_bike[i] else LANE_SHIFT_CAR
                        target_off = best_sign * shift_mag * best_shape
                    else:
                        # Adjacent lane is occupied -> Stay straight on road through pothole
                        target_off = 0.0

            # Step 4: Exponential smoothing for silky smooth transition
            prev_offset = cur_off[i]
            new_offset  = prev_offset + (target_off - prev_offset) * SMOOTH_RATE

            if abs(new_offset) < 0.003:
                new_offset = 0.0
            cur_off[i] = new_offset

            # Step 5: Apply to local PROTO translation (or fallback to Solid delta)
            if pt:
                pt.setSFVec3f([0.0, new_offset, 0.0])
            elif veh_trans[i]:
                delta = new_offset - prev_offset
                if abs(delta) > 0.001:
                    veh_trans[i].setSFVec3f([vx + delta * nx, vy + delta * ny, vz])


if __name__ == '__main__':
    main()
