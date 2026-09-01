"""
pothole_controller.py — Curve-Perfect, Dynamically-Yielding Pothole Avoidance.

SAFETY GUARANTEES:
1. Curve-Perfect Detection: Uses the exact road normal at the pothole to calculate 
   true lane occupancy, completely eliminating false positives on sharp curves where 
   a car in Lane 1 would previously think a Lane 0 pothole was in its path.
2. Dynamic Yielding: Evaluates adjacent lane occupancy (is_blocked) continuously.
   If a neighbor pulls up mid-swerve, the car aborts and returns to its lane safely.
3. Rate-Limited Steering: Max lateral delta is strictly clamped to <= 0.025m per 32ms frame.
4. Exact Lane Alignment: Only triggers for vehicles traveling in Lane 0. Shifts +1.20m LEFT.
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

# True road direction vector at each pothole (dx, dy)
POTHOLE_DIRS = [
    (0.9951, 0.0994), (0.9951, 0.0994), (-0.9951, -0.0994), (-0.9951, -0.0994),
    (0.6717, 0.7408), (0.9421, 0.3353), (1.0000, 0.0000), (0.8034, -0.5955),
    (0.0000, -1.0000), (-0.3374, -0.9414), (-1.0000, 0.0000), (-0.5138, 0.8579),
    (0.0000, -1.0000), (0.0000, -1.0000), (0.7438, -0.6684), (0.9703, -0.2419),
    (1.0000, 0.0000), (0.0000, 1.0000),
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


def shift_shape(d_fwd):
    """Smooth 0 -> 1 -> 0 easing curve for lane-shift magnitude.
    Splits the approach and recovery into two independent quarter-sine eases,
    so the offset reaches 100% precisely at d_fwd == 0 (at the pothole).
    """
    if d_fwd >= 0.0:
        # Approach phase: 0 at DETECTION_DIST -> 1 at the pothole (d_fwd=0)
        t = 1.0 - (d_fwd / DETECTION_DIST)
    else:
        # Recovery phase: 1 at the pothole (d_fwd=0) -> 0 at RECOVERY_DIST
        t = 1.0 - (d_fwd / RECOVERY_DIST)
    t = max(0.0, min(1.0, t))
    return math.sin(t * math.pi / 2.0)


def yaw_from_rotation_field(rot, fallback=0.0):
    """Extract true car-front heading in Webots XY from rotation field."""
    ax, ay, az, angle = rot
    if abs(az) < 0.5:
        return fallback
    yaw = angle if az > 0 else -angle
    return -yaw


def main():
    robot    = Supervisor()
    timestep = int(robot.getBasicTimeStep()) or 32

    print(f"[PotholeCtrl] Curve-Perfect Dynamic Pothole Supervisor Online ({len(POTHOLES)} hazards).")

    veh_trans   = [None] * MAX_VEH
    veh_rot     = [None] * MAX_VEH
    proto_trans = [None] * MAX_VEH
    base_y_off  = [0.0]  * MAX_VEH
    veh_is_bike = [False] * MAX_VEH
    cur_off     = [0.0]  * MAX_VEH
    last_heading = [0.0] * MAX_VEH

    active_pot_idx = [None]  * MAX_VEH

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
                            pt_field = proto.getField("translation")
                            if pt_field:
                                proto_trans[i] = pt_field
                                # Save the initial base offset ONLY once
                                if base_y_off[i] == 0.0:
                                    base_y_off[i] = pt_field.getSFVec3f()[1]
                            
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
                    rot = vr.getSFRotation()
                    h = yaw_from_rotation_field(rot, fallback=last_heading[i])
                    last_heading[i] = h
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
                
                d_fwd = (px - vx) * ux + (py - vy) * uy

                if d_fwd < RECOVERY_DIST:
                    # Cleared pothole completely
                    active_pot_idx[i] = None
                    target_off = 0.0
                else:
                    # Dynamically check for adjacent lane blockages continuously!
                    blocked = False
                    for j, ((ox, oy, _), jh) in active.items():
                        if j == i: continue
                        # Same direction only
                        dot_h = math.cos(h) * math.cos(jh) + math.sin(h) * math.sin(jh)
                        if dot_h < 0.5: continue

                        odx = ox - vx
                        ody = oy - vy
                        ofwd = odx * ux + ody * uy
                        olat = odx * nx + ody * ny

                        # Neighbor in Lane 1 alongside (-4.5m to +7.0m, olat in [0.7m, 3.2m])
                        if -4.5 <= ofwd <= 7.0 and 0.70 <= olat <= 3.20:
                            blocked = True
                            break

                    shape = shift_shape(d_fwd)

                    if not blocked:
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
                        # Fwd distance based on car's heading
                        d_fwd = (px - vx) * ux + (py - vy) * uy
                        
                        # True road lateral distance based on POTHOLE'S road direction
                        # road_nx = -dy, road_ny = dx (Left relative to road direction)
                        p_dx, p_dy = POTHOLE_DIRS[p_idx]
                        road_nx = -p_dy
                        road_ny = p_dx
                        
                        true_lat_dist = (vx - px) * road_nx + (vy - py) * road_ny

                        # EXPECTED DEVIATION MATH
                        # Calculate the exact lateral deviation expected if the car is perfectly
                        # following the curve, using the angle between pothole tangent and car heading.
                        cross = p_dx * uy - p_dy * ux
                        dot = p_dx * ux + p_dy * uy
                        angle = math.atan2(cross, dot)
                        expected_dev = d_fwd * math.tan(angle / 2.0)
                        
                        lane_offset = true_lat_dist - expected_dev

                        # Trigger ONLY if the car is physically in the same lane (Lane 0)
                        if 0.0 < d_fwd <= DETECTION_DIST and abs(lane_offset) < 1.35:
                            if d_fwd < best_fwd:
                                best_fwd = d_fwd
                                best_pot = p_idx

                    if best_pot is not None:
                        active_pot_idx[i] = best_pot
                        
                        # Immediately evaluate block status so we can set target_off
                        blocked = False
                        for j, ((ox, oy, _), jh) in active.items():
                            if j == i: continue
                            dot_h = math.cos(h) * math.cos(jh) + math.sin(h) * math.sin(jh)
                            if dot_h < 0.5: continue

                            odx = ox - vx
                            ody = oy - vy
                            ofwd = odx * ux + ody * uy
                            olat = odx * nx + ody * ny

                            if -4.5 <= ofwd <= 7.0 and 0.70 <= olat <= 3.20:
                                blocked = True
                                break

                        shape = shift_shape(best_fwd)

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

            # Step 4: Apply gentle lateral offset to vehicle's child PROTO (local frame)
            # This completely prevents world-coordinate accumulation bugs!
            pt = proto_trans[i]
            if pt:
                # Webots vehicle local frame: X=forward, Y=left, Z=up
                # We just write [0, offset, 0] to shift it laterally
                curr_local = pt.getSFVec3f()
                pt.setSFVec3f([curr_local[0], base_y_off[i] + cur_off[i], curr_local[2]])


if __name__ == '__main__':
    main()
