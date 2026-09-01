"""
pothole_controller.py — Rock-Solid, On-Road Pothole Avoidance (Zero Accumulation, Zero Offroad).

ARCHITECTURE:
1. Applies lateral lane shift directly to the vehicle's child PROTO local translation [0, offset, 0].
   - Local +Y in Webots vehicle coordinate frame is ALWAYS the vehicle's left (towards adjacent asphalt lane).
   - Local frame automatically follows vehicle heading through curves, turns, and straightaways.
   - Parent SUMO_VEHICLE translation is NEVER modified or corrupted — zero fighting with sumo_supervisor, zero teleporting, zero shaking.
   - Zero world coordinate accumulation: offset is an absolute local displacement [0, offset, 0] that decays back to [0, 0, 0].
2. Adjacent Lane Clearance:
   - If adjacent Lane 1 is occupied by a vehicle alongside (-6m to +9m, olat > 0.6m): DO NOT SWERVE (stays at [0,0,0], drives straight through).
   - If adjacent Lane 1 is clear: Smoothly shifts left into Lane 1 (1.20m on pure asphalt), bypasses the pothole, and returns to [0,0,0].
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

DETECTION_DIST   = 13.0   # metres ahead to begin lane shift
RECOVERY_DIST    = -2.0   # metres past to complete return
TOTAL_SPAN       = DETECTION_DIST - RECOVERY_DIST  # 15.0m
LANE_SHIFT_CAR   = 1.20   # metres LEFT into Lane 1 (stays 100% on asphalt)
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

    print(f"[PotholeCtrl] Local-Frame Lane-Shift Supervisor Online ({len(POTHOLES)} potholes).")

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
            nx = -uy   # Left lateral unit vector in world XY
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

                    # Check if pothole is in path
                    if RECOVERY_DIST <= d_fwd <= DETECTION_DIST and abs(d_lat) < 1.70:
                        if abs(d_fwd) < best_dist:
                            best_dist = abs(d_fwd)
                            progress = (DETECTION_DIST - d_fwd) / TOTAL_SPAN
                            progress = max(0.0, min(1.0, progress))
                            best_shape = math.sin(progress * math.pi)

                if best_shape > 0.0:
                    # Step 3: Adjacent Lane Clearance Check
                    # Check if any vehicle is in Lane 1 beside us (olat in [0.5m, 3.2m], ofwd in [-5m, +8m])
                    lane_1_clear = True
                    for j, (ox, oy, _) in active_positions.items():
                        if j == i:
                            continue
                        odx = ox - vx
                        ody = oy - vy
                        ofwd = odx * ux + ody * uy
                        olat = odx * nx + ody * ny

                        if -5.5 <= ofwd <= 8.5 and 0.55 <= olat <= 3.2:
                            lane_1_clear = False
                            break

                    if lane_1_clear:
                        # Shift into Lane 1 (local +Y is vehicle's left = adjacent asphalt lane)
                        shift_mag = LANE_SHIFT_BIKE if veh_is_bike[i] else LANE_SHIFT_CAR
                        target_off = shift_mag * best_shape
                    else:
                        # Adjacent lane is occupied -> Stay strictly at 0 (drive straight through pothole)
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
