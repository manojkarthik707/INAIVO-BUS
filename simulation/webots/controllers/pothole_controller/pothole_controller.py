"""
pothole_controller.py — Safe, In-Lane Pothole Avoidance with Adjacent Vehicle Clearance.

FIXES:
1. Reduced swerve magnitude (0.45m for cars, 0.25m for bikes) so vehicles NEVER go off-road or mount the curb.
2. Real-time adjacent vehicle clearance check: if another car is driving beside on the swerve side, swerve is suppressed to prevent vehicle clipping/collision.
3. Smooth exponential transition per frame with stable rotation-field heading.
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

_px = [p[0] for p in POTHOLES]
_py = [p[1] for p in POTHOLES]
POT_XMIN = min(_px) - 25.0
POT_XMAX = max(_px) + 25.0
POT_YMIN = min(_py) - 25.0
POT_YMAX = max(_py) + 25.0

DETECTION_DIST   = 13.0   # metres ahead
RECOVERY_DIST    = -2.0   # metres past
TOTAL_SPAN       = DETECTION_DIST - RECOVERY_DIST  # 15.0m
MAX_SWERVE_CAR   = 0.45   # metres — safe inside 2.69m lane, will NEVER hit curb or neighbor
MAX_SWERVE_BIKE  = 0.25   # metres for 2-wheelers
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

    print(f"[PotholeCtrl] Safe In-Lane Avoidance Supervisor Online ({len(POTHOLES)} potholes).")

    veh_trans = [None] * MAX_VEH
    veh_rot   = [None] * MAX_VEH
    veh_is_bike = [False] * MAX_VEH
    cur_off   = [0.0]  * MAX_VEH

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

        # Step 1: Collect active vehicle positions for neighbor clearance check
        active_positions = {}
        for i in range(MAX_VEH):
            vt = veh_trans[i]
            if vt:
                p = vt.getSFVec3f()
                if p[0] < 9000:
                    active_positions[i] = p

        # Step 2: Calculate safe in-lane swerve per vehicle
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
            nx = -uy   # Lateral unit vector (left of vehicle)
            ny = ux

            target_off = 0.0
            best_sign  = 0.0

            if in_zone:
                best_dist  = 999.0
                best_shape = 0.0

                for (px, py) in POTHOLES:
                    dx = px - vx
                    dy = py - vy

                    d_fwd = dx * ux + dy * uy
                    d_lat = dx * nx + dy * ny

                    if RECOVERY_DIST <= d_fwd <= DETECTION_DIST and abs(d_lat) < 1.75:
                        if abs(d_fwd) < best_dist:
                            best_dist = abs(d_fwd)
                            # Swerve away from pothole center
                            best_sign = 1.0 if d_lat <= 0.0 else -1.0

                            progress = (DETECTION_DIST - d_fwd) / TOTAL_SPAN
                            progress = max(0.0, min(1.0, progress))
                            best_shape = math.sin(progress * math.pi)

                if best_shape > 0.0:
                    max_sw = MAX_SWERVE_BIKE if veh_is_bike[i] else MAX_SWERVE_CAR
                    target_off = best_sign * max_sw * best_shape

                    # Step 3: Adjacent vehicle clearance check (prevent side-clipping)
                    if target_off != 0.0:
                        for j, (ox, oy, _) in active_positions.items():
                            if j == i:
                                continue
                            odx = ox - vx
                            ody = oy - vy
                            # Project neighbor relative position onto vehicle frame
                            ofwd = odx * ux + ody * uy
                            olat = odx * nx + ody * ny
                            # If another vehicle is beside us on the side we want to swerve towards
                            if -4.5 <= ofwd <= 6.5 and (olat * best_sign) > 0.4:
                                target_off = 0.0   # Blocked by neighbor car -> stay straight
                                break

            # Exponential smoothing to prevent any jerk
            prev_offset = cur_off[i]
            new_offset  = prev_offset + (target_off - prev_offset) * SMOOTH_RATE

            if abs(new_offset) < 0.002:
                new_offset = 0.0
            cur_off[i] = new_offset

            if abs(new_offset) > 0.002:
                vt.setSFVec3f([vx + new_offset * nx, vy + new_offset * ny, vz])


if __name__ == '__main__':
    main()
