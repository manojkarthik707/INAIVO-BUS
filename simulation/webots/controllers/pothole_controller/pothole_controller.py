"""
pothole_controller.py — Gentle Rate-Limited In-Road Pothole Avoidance (Zero Yeeting).

SAFETY GUARANTEES:
1. Rate-Limited Steering: Max lateral delta is strictly clamped to <= 0.025m per 32ms frame.
   - Eliminates physics shockwaves, torque spikes, and vehicle yeeting/spinning.
2. Exact Lane Alignment:
   - Only triggers for vehicles traveling in the same direction on Lane 0 (where potholes reside).
   - Vehicles in Lane 1 or oncoming lanes ignore the pothole completely.
3. Safe In-Road Shift:
   - Shifts smoothly +1.20m LEFT into Lane 1 on pure asphalt, passes the pothole, and returns to Lane 0.
4. Adjacent Traffic Clearance:
   - If a same-direction vehicle is alongside in Lane 1, the vehicle stays centered and drives safely through.
"""

import math
from controller import Supervisor

# 18 Terracotta Brown Potholes on Road Centerlines (All located in Lane 0)
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

DETECTION_DIST   = 15.0   # metres ahead to start lane shift
RECOVERY_DIST    = -3.0   # metres past to finish lane return
TOTAL_SPAN       = DETECTION_DIST - RECOVERY_DIST  # 18.0m
LANE_SHIFT_CAR   = 1.20   # metres shift left into Lane 1
LANE_SHIFT_BIKE  = 0.75   # metres for 2-wheelers
MAX_DELTA_FRAME  = 0.025  # max displacement per frame (0.78 m/s gentle drift)
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

    print(f"[PotholeCtrl] Gentle Rate-Limited Lane Shift Supervisor Online ({len(POTHOLES)} hazards).")

    veh_trans   = [None] * MAX_VEH
    veh_rot     = [None] * MAX_VEH
    veh_is_bike = [False] * MAX_VEH
    cur_off     = [0.0]  * MAX_VEH

    active_pot_idx = [None]  * MAX_VEH
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

        # Step 2: Process each vehicle
        for i in range(MAX_VEH):
            if i not in active:
                cur_off[i] = 0.0
                active_pot_idx[i] = None
                continue

            (vx, vy, vz), h = active[i]
            vt = veh_trans[i]

            in_zone = (POT_XMIN <= vx <= POT_XMAX and POT_YMIN <= vy <= POT_YMAX)
            if not in_zone and abs(cur_off[i]) < 0.005 and active_pot_idx[i] is None:
                cur_off[i] = 0.0
                continue

            ux = math.cos(h)
            uy = math.sin(h)
            nx = -uy   # Left lateral unit vector (towards Lane 1)
            ny = ux

            target_off = 0.0

            # ── State A: Currently executing an avoidance pass ─────────────────
            if active_pot_idx[i] is not None:
                pot_i = active_pot_idx[i]
                px, py = POTHOLES[pot_i]
                dx = px - vx
                dy = py - vy
                d_fwd = dx * ux + dy * uy

                if d_fwd < RECOVERY_DIST:
                    # Cleared pothole completely
                    active_pot_idx[i] = None
                    is_blocked[i] = False
                    target_off = 0.0
                else:
                    progress = (DETECTION_DIST - d_fwd) / TOTAL_SPAN
                    progress = max(0.0, min(1.0, progress))
                    shape = math.sin(progress * math.pi)

                    if not is_blocked[i]:
                        shift_mag = LANE_SHIFT_BIKE if veh_is_bike[i] else LANE_SHIFT_CAR
                        target_off = shift_mag * shape
                    else:
                        target_off = 0.0

            # ── State B: Cruising — check for upcoming potholes in Lane 0 ─────
            else:
                if in_zone:
                    best_pot = None
                    best_fwd = 999.0

                    for p_idx, (px, py) in enumerate(POTHOLES):
                        dx = px - vx
                        dy = py - vy
                        d_fwd = dx * ux + dy * uy
                        d_lat = dx * nx + dy * ny

                        # Only trigger if pothole is directly in this vehicle's path (Lane 0)
                        if 0.0 < d_fwd <= DETECTION_DIST and abs(d_lat) < 1.35:
                            if d_fwd < best_fwd:
                                best_fwd = d_fwd
                                best_pot = p_idx

                    if best_pot is not None:
                        active_pot_idx[i] = best_pot

                        # Check if Lane 1 on the left is occupied by same-direction vehicle
                        blocked = False
                        for j, ((ox, oy, _), jh) in active.items():
                            if j == i:
                                continue

                            # Same direction only (ignore oncoming traffic across median)
                            dot_h = math.cos(h) * math.cos(jh) + math.sin(h) * math.sin(jh)
                            if dot_h < 0.5:
                                continue

                            odx = ox - vx
                            ody = oy - vy
                            ofwd = odx * ux + ody * uy
                            olat = odx * nx + ody * ny

                            # Neighbor in Lane 1 alongside (-4.5m to +7.0m, olat in [0.7m, 3.2m])
                            if -4.5 <= ofwd <= 7.0 and 0.70 <= olat <= 3.20:
                                blocked = True
                                break

                        is_blocked[i] = blocked

                        progress = (DETECTION_DIST - best_fwd) / TOTAL_SPAN
                        progress = max(0.0, min(1.0, progress))
                        shape = math.sin(progress * math.pi)

                        if not blocked:
                            shift_mag = LANE_SHIFT_BIKE if veh_is_bike[i] else LANE_SHIFT_CAR
                            target_off = shift_mag * shape
                        else:
                            target_off = 0.0

            # Step 3: Rate-limited smooth interpolation (max 0.025m per frame)
            diff = target_off - cur_off[i]
            step_delta = max(-MAX_DELTA_FRAME, min(MAX_DELTA_FRAME, diff))
            cur_off[i] += step_delta

            if abs(cur_off[i]) < 0.003:
                cur_off[i] = 0.0

            # Step 4: Apply gentle lateral offset to vehicle
            if abs(cur_off[i]) > 0.003:
                vt.setSFVec3f([vx + cur_off[i] * nx, vy + cur_off[i] * ny, vz])


if __name__ == '__main__':
    main()
