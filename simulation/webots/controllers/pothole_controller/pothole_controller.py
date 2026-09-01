"""
pothole_controller.py — Silky-Smooth Continuous Pothole Avoidance Supervisor.

ELIMINATED SHAKING & JITTER:
1. Runs EVERY timestep (no skipped frames) to stay perfectly in sync with sumo_supervisor.
2. Reads true vehicle heading from the rotation field (no noisy displacement calculations).
3. Applies a continuous sine-bell lateral offset profile with exponential smoothing.
4. Bounding-box fast reject for optimal simulation performance with 100 vehicles.
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

# Fast bounding-box rejection margin
_px = [p[0] for p in POTHOLES]
_py = [p[1] for p in POTHOLES]
POT_XMIN = min(_px) - 25.0
POT_XMAX = max(_px) + 25.0
POT_YMIN = min(_py) - 25.0
POT_YMAX = max(_py) + 25.0

DETECTION_DIST = 14.0   # Start swerve 14m before pothole
RECOVERY_DIST  = -2.5   # Complete lane return 2.5m past pothole
TOTAL_SPAN     = DETECTION_DIST - RECOVERY_DIST  # 16.5m
MAX_SWERVE     = 1.30   # Max lateral displacement in metres (clears 0.8m radius easily)
SMOOTH_RATE    = 0.22   # Exponential smoothing per 32ms frame (~150ms time constant)
MAX_VEH        = 100


def get_vehicle_heading(vr):
    """Extract true car-front heading in Webots XY coordinates from rotation field."""
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

    print(f"[PotholeCtrl] Monitoring {len(POTHOLES)} potholes across map...")

    veh_trans = [None] * MAX_VEH
    veh_rot   = [None] * MAX_VEH
    cur_off   = [0.0]  * MAX_VEH

    def resolve_vehicles():
        for i in range(MAX_VEH):
            if veh_trans[i] is None:
                node = robot.getFromDef(f"SUMO_VEHICLE{i}")
                if node:
                    veh_trans[i] = node.getField("translation")
                    veh_rot[i]   = node.getField("rotation")

    resolve_vehicles()
    print(f"[PotholeCtrl] {sum(1 for t in veh_trans if t)} vehicle refs cached. Running smooth swerve.")

    step = 0
    while robot.step(timestep) != -1:
        step += 1

        # Periodically resolve any newly connected vehicles
        if step % 90 == 0:
            resolve_vehicles()

        for i in range(MAX_VEH):
            vt = veh_trans[i]
            vr = veh_rot[i]
            if not vt or not vr:
                continue

            pos = vt.getSFVec3f()
            vx, vy, vz = pos

            # Parked/inactive vehicle
            if vx > 9000:
                cur_off[i] = 0.0
                continue

            # Fast bounding box reject — if outside the pothole zone and no active offset, skip
            in_zone = (POT_XMIN <= vx <= POT_XMAX and POT_YMIN <= vy <= POT_YMAX)
            if not in_zone and abs(cur_off[i]) < 0.005:
                continue

            # Heading and normal vectors
            h = get_vehicle_heading(vr)
            ux = math.cos(h)
            uy = math.sin(h)
            nx = -uy   # Lateral unit vector (left of vehicle)
            ny = ux

            target_off = 0.0

            if in_zone:
                # Find closest pothole in front of this vehicle
                best_dist = 999.0
                best_sign = 0.0
                best_shape = 0.0

                for (px, py) in POTHOLES:
                    dx = px - vx
                    dy = py - vy

                    # Distance projection onto vehicle coordinate frame
                    d_fwd = dx * ux + dy * uy
                    d_lat = dx * nx + dy * ny

                    # Check if pothole is directly in front of this vehicle's path
                    if RECOVERY_DIST <= d_fwd <= DETECTION_DIST and abs(d_lat) < 1.85:
                        if abs(d_fwd) < best_dist:
                            best_dist = abs(d_fwd)
                            # Swerve away from pothole:
                            # if pothole is right or center (d_lat <= 0) -> swerve left (+1.0)
                            # if pothole is left (d_lat > 0) -> swerve right (-1.0)
                            best_sign = 1.0 if d_lat <= 0.0 else -1.0

                            # Smooth sine bell curve across the approach window
                            progress = (DETECTION_DIST - d_fwd) / TOTAL_SPAN
                            progress = max(0.0, min(1.0, progress))
                            best_shape = math.sin(progress * math.pi)

                if best_shape > 0.0:
                    target_off = best_sign * MAX_SWERVE * best_shape

            # Exponential smoothing to eliminate any frame-to-frame jerk
            prev_offset = cur_off[i]
            new_offset  = prev_offset + (target_off - prev_offset) * SMOOTH_RATE

            if abs(new_offset) < 0.003:
                new_offset = 0.0
            cur_off[i] = new_offset

            # Apply smooth lateral displacement on top of road position
            if abs(new_offset) > 0.003:
                vt.setSFVec3f([vx + new_offset * nx, vy + new_offset * ny, vz])


if __name__ == '__main__':
    main()
