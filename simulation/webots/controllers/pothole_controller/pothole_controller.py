"""
pothole_controller.py — Precision Closed-Form Pothole Avoidance & Lane Change.

ALGORITHM:
1. Closed-Form Trajectory: Direct sine-bell offset applied to fresh SUMO lane coordinates.
   - Zero accumulation, zero drift, zero physics matrix instability.
2. State-Locked Direction:
   - When approaching a pothole at 14m, locks escape direction (+LEFT into Lane 1, or -RIGHT into Lane 0).
   - Never re-evaluates or flips direction mid-curve (eliminates all lane shaking/jitter).
3. Same-Direction Target-Lane Clearance:
   - Checks if same-direction traffic (dot_heading > 0.5) is present in the target lane.
   - If free: executes a smooth 1.35m shift into the adjacent asphalt lane, passes the pothole, and returns.
   - If occupied: drives safely straight through without colliding.
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

DETECTION_DIST   = 14.0   # metres ahead to start lane shift
RECOVERY_DIST    = -2.5   # metres past to finish lane return
TOTAL_SPAN       = DETECTION_DIST - RECOVERY_DIST  # 16.5m
LANE_SHIFT_CAR   = 1.35   # metres shift into adjacent asphalt lane
LANE_SHIFT_BIKE  = 0.85   # metres for 2-wheelers
MAX_VEH          = 100


def get_vehicle_heading(vr):
    """Extract true car-front heading in Webots XY from rotation field."""
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

    print(f"[PotholeCtrl] Precision Lane-Shift Supervisor Online ({len(POTHOLES)} potholes).")

    veh_trans   = [None] * MAX_VEH
    veh_rot     = [None] * MAX_VEH
    veh_is_bike = [False] * MAX_VEH

    # State tracking per vehicle
    active_pot_idx = [None]  * MAX_VEH
    locked_sign    = [0.0]   * MAX_VEH
    is_blocked     = [False] * MAX_VEH

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

        # Step 2: Process each active vehicle
        for i in range(MAX_VEH):
            if i not in active:
                active_pot_idx[i] = None
                continue

            (vx, vy, vz), h = active[i]
            vt = veh_trans[i]

            in_zone = (POT_XMIN <= vx <= POT_XMAX and POT_YMIN <= vy <= POT_YMAX)
            if not in_zone and active_pot_idx[i] is None:
                continue

            ux = math.cos(h)
            uy = math.sin(h)
            nx = -uy   # Lateral unit vector (+nx = Left into Lane 1, -nx = Right into Lane 0)
            ny = ux

            target_off = 0.0

            # ── State A: Currently executing a locked pothole lane shift ──────
            if active_pot_idx[i] is not None:
                pot_i = active_pot_idx[i]
                px, py = POTHOLES[pot_i]
                dx = px - vx
                dy = py - vy
                d_fwd = dx * ux + dy * uy

                if d_fwd < RECOVERY_DIST:
                    # Completed passing the pothole -> reset state to cruise
                    active_pot_idx[i] = None
                    locked_sign[i] = 0.0
                    is_blocked[i] = False
                    target_off = 0.0
                else:
                    progress = (DETECTION_DIST - d_fwd) / TOTAL_SPAN
                    progress = max(0.0, min(1.0, progress))
                    shape = math.sin(progress * math.pi)

                    if not is_blocked[i]:
                        shift_mag = LANE_SHIFT_BIKE if veh_is_bike[i] else LANE_SHIFT_CAR
                        target_off = locked_sign[i] * shift_mag * shape
                    else:
                        target_off = 0.0

            # ── State B: Cruising — detect upcoming potholes ──────────────────
            else:
                if in_zone:
                    best_pot  = None
                    best_fwd  = 999.0
                    best_dlat = 0.0

                    for p_idx, (px, py) in enumerate(POTHOLES):
                        dx = px - vx
                        dy = py - vy
                        d_fwd = dx * ux + dy * uy
                        d_lat = dx * nx + dy * ny

                        # Check if approaching pothole in vehicle's forward corridor
                        if 0.0 < d_fwd <= DETECTION_DIST and abs(d_lat) < 1.75:
                            if d_fwd < best_fwd:
                                best_fwd  = d_fwd
                                best_pot  = p_idx
                                best_dlat = d_lat

                    if best_pot is not None:
                        # Lock in this pothole maneuver
                        active_pot_idx[i] = best_pot

                        # Determine escape direction:
                        # Pothole on vehicle's left (d_lat > 0) -> shift RIGHT (-1.0 into outer lane)
                        # Pothole on vehicle's right or centered (d_lat <= 0) -> shift LEFT (+1.0 into inner lane)
                        if best_dlat > 0.05:
                            s = -1.0
                        else:
                            s = 1.0
                        locked_sign[i] = s

                        # Check if target lane is blocked by same-direction vehicle
                        blocked = False
                        for j, ((ox, oy, _), jh) in active.items():
                            if j == i:
                                continue

                            # Same direction vehicles only (ignore oncoming traffic across median)
                            dot_h = math.cos(h) * math.cos(jh) + math.sin(h) * math.sin(jh)
                            if dot_h < 0.5:
                                continue

                            odx = ox - vx
                            ody = oy - vy
                            ofwd = odx * ux + ody * uy
                            olat = odx * nx + ody * ny

                            # Neighbor alongside in target lane (-4.5m to +7.0m, olat on swerve side)
                            if -4.5 <= ofwd <= 7.0 and (olat * s) > 0.65:
                                blocked = True
                                break

                        is_blocked[i] = blocked

                        progress = (DETECTION_DIST - best_fwd) / TOTAL_SPAN
                        progress = max(0.0, min(1.0, progress))
                        shape = math.sin(progress * math.pi)

                        if not blocked:
                            shift_mag = LANE_SHIFT_BIKE if veh_is_bike[i] else LANE_SHIFT_CAR
                            target_off = s * shift_mag * shape
                        else:
                            target_off = 0.0

            # Step 3: Apply exact closed-form offset to vehicle translation
            if abs(target_off) > 0.01:
                vt.setSFVec3f([vx + target_off * nx, vy + target_off * ny, vz])


if __name__ == '__main__':
    main()
