"""
number_plate_controller.py — Indian License Plate Supervisor (stable, no spinning).

KEY FIX: Use rotation field (yaw) for heading, corrected by -yaw convention.
  From math verification:
    SUMO North (0°)   → Webots yaw=-90°  → correct heading = -(-90°) = +90° = North ✓
    SUMO East  (90°)  → Webots yaw=0°    → correct heading = -(0°)   = 0°   = East  ✓
    SUMO South (180°) → Webots yaw=+90°  → correct heading = -(+90°) = -90° = South ✓
    SUMO West  (270°) → Webots yaw=+180° → correct heading = -(180°) = 180° = West  ✓

  DO NOT use displacement/velocity heading — pothole_controller modifies vehicle
  translation laterally, corrupting the displacement vector and causing heading
  to spin/circle continuously.
"""

import math
from controller import Supervisor

INDIAN_STATES = ["TN", "KA", "MH", "DL", "TS", "GJ", "KL", "AP", "WB", "HR"]
SERIES = ["AB", "CD", "EF", "GH", "JK", "LM", "NP", "QR", "ST", "UV", "WX", "YZ"]

def get_plate(v_idx):
    state  = INDIAN_STATES[v_idx % len(INDIAN_STATES)]
    rto    = f"{(v_idx * 3 + 1) % 99 + 1:02d}"
    series = SERIES[(v_idx // len(INDIAN_STATES)) % len(SERIES)]
    num    = f"{(v_idx * 127 + 1001) % 9000 + 1000:04d}"
    return f"{state} {rto} {series} {num}"

# ── Plate geometry ──────────────────────────────────────────────────────────
# Box size in Webots XYZ (Z = up):
#   X = depth (thin, faces heading direction)
#   Y = lateral width
#   Z = vertical height
PLATE_DEPTH  = 0.030
PLATE_WIDTH  = 1.04    # 2× real plate width for visibility at distance
PLATE_HEIGHT = 0.230   # 2× real plate height

# Offsets from vehicle Solid centre in the CAR-FRONT direction
FRONT_OFFSET =  2.10   # positive = ahead of Solid centre
REAR_OFFSET  = -2.00   # negative = behind Solid centre

PLATE_Z_OFFSET = -0.05  # plate Z = vehicle Z + this (bumper is slightly below CG)

MAX_VEH   = 100
TEX_DIR   = "textures/plates"
PARKED_X  = 10500.0


def plate_vrml(def_name, tex_path):
    return (
        f"DEF {def_name} Pose {{\n"
        f"  translation {PARKED_X} 0 0.4\n"
        f"  rotation 0 0 1 0\n"
        f"  children [\n"
        f"    Shape {{\n"
        f"      appearance PBRAppearance {{\n"
        f"        baseColorMap ImageTexture {{\n"
        f"          url [ \"{tex_path}\" ]\n"
        f"        }}\n"
        f"        roughness 0.3\n"
        f"        metalness 0.0\n"
        f"      }}\n"
        f"      geometry Box {{\n"
        f"        size {PLATE_DEPTH} {PLATE_WIDTH} {PLATE_HEIGHT}\n"
        f"      }}\n"
        f"    }}\n"
        f"  ]\n"
        f"}}\n"
    )


def yaw_from_rotation_field(rot):
    """
    Extract Webots yaw from the rotation field [ax, ay, az, angle].
    SUMO supervisor always produces a pure Z-axis rotation (az ≈ ±1).
    Yaw = signed angle:  positive az → yaw = +angle,  negative az → yaw = -angle.
    
    Then: correct_car_heading = -yaw
    (Verified for all 4 SUMO cardinal directions.)
    """
    ax, ay, az, angle = rot
    if az > 0.5:
        yaw = angle
    elif az < -0.5:
        yaw = -angle
    else:
        # Unusual — non-Z axis (shouldn't happen for SUMO vehicles on flat roads)
        # Fall back to 0
        yaw = 0.0
    return -yaw   # negate to get car-front heading


def main():
    robot    = Supervisor()
    timestep = int(robot.getBasicTimeStep()) or 32

    root_ch = robot.getRoot().getField("children")
    print("[PlateCtrl] Injecting 200 Pose plate nodes...")
    for i in range(MAX_VEH):
        tex = f"{TEX_DIR}/plate_{i:03d}.png"
        root_ch.importMFNodeFromString(-1, plate_vrml(f"PLATE_F_{i}", tex))
        root_ch.importMFNodeFromString(-1, plate_vrml(f"PLATE_R_{i}", tex))

    # ── Cache all field refs at startup ───────────────────────────────────
    pf_trans, pf_rot, pr_trans, pr_rot = [], [], [], []
    for i in range(MAX_VEH):
        fn = robot.getFromDef(f"PLATE_F_{i}")
        rn = robot.getFromDef(f"PLATE_R_{i}")
        pf_trans.append(fn.getField("translation") if fn else None)
        pf_rot.append(  fn.getField("rotation")    if fn else None)
        pr_trans.append(rn.getField("translation") if rn else None)
        pr_rot.append(  rn.getField("rotation")    if rn else None)

    veh_trans = [None] * MAX_VEH
    veh_rot   = [None] * MAX_VEH

    def resolve_vehicles():
        for i in range(MAX_VEH):
            if veh_trans[i] is None:
                nd = robot.getFromDef(f"SUMO_VEHICLE{i}")
                if nd:
                    veh_trans[i] = nd.getField("translation")
                    veh_rot[i]   = nd.getField("rotation")
                    # Try to blank built-in white plate text (if PROTO exposes it)
                    ch_f = nd.getField("children")
                    if ch_f and ch_f.getCount() > 0:
                        proto = ch_f.getMFNode(0)
                        if proto:
                            for fname in ["frontLicensePlate", "rearLicensePlate",
                                          "licensePlate", "plateText"]:
                                f2 = proto.getField(fname)
                                if f2:
                                    try: f2.setSFString(" ")
                                    except Exception: pass

    resolve_vehicles()
    resolved = sum(1 for t in veh_trans if t)
    print(f"[PlateCtrl] {resolved}/{MAX_VEH} nodes cached. Running.")

    step = 0
    debug_printed = False

    while robot.step(timestep) != -1:
        step += 1
        if step % 90 == 0:
            resolve_vehicles()

        for i in range(MAX_VEH):
            vt = veh_trans[i]
            vr = veh_rot[i]
            if not vt or not vr:
                continue

            pos = vt.getSFVec3f()
            vx, vy, vz = pos

            # Park plates for idle/hidden vehicles
            if vx > 9000:
                t = pf_trans[i]
                if t: t.setSFVec3f([PARKED_X + i, 0.0, 0.4])
                t = pr_trans[i]
                if t: t.setSFVec3f([PARKED_X + i, 0.5, 0.4])
                continue

            # ── Heading from rotation field (stable, not corrupted by pothole) ──
            rot = vr.getSFRotation()
            h   = yaw_from_rotation_field(rot)

            fx  = math.cos(h)
            fy  = math.sin(h)
            pz  = vz + PLATE_Z_OFFSET

            # Front plate
            pft = pf_trans[i]
            pfr = pf_rot[i]
            if pft:
                pft.setSFVec3f([vx + fx * FRONT_OFFSET,
                                vy + fy * FRONT_OFFSET,
                                pz])
            if pfr:
                pfr.setSFRotation([0, 0, 1, h])

            # Rear plate
            prt = pr_trans[i]
            prr = pr_rot[i]
            if prt:
                prt.setSFVec3f([vx + fx * REAR_OFFSET,
                                vy + fy * REAR_OFFSET,
                                pz])
            if prr:
                prr.setSFRotation([0, 0, 1, h + math.pi])

        # One-time debug: print heading for first 3 active vehicles at ~5s
        if not debug_printed and step == 150:
            debug_printed = True
            for i in range(MAX_VEH):
                if veh_trans[i]:
                    pos = veh_trans[i].getSFVec3f()
                    if pos[0] < 9000 and veh_rot[i]:
                        rot = veh_rot[i].getSFRotation()
                        h = yaw_from_rotation_field(rot)
                        print(f"[PlateCtrl] VEH{i}: ({pos[0]:.1f},{pos[1]:.1f},{pos[2]:.2f})"
                              f"  rot=[{rot[0]:.1f},{rot[1]:.1f},{rot[2]:.1f},{math.degrees(rot[3]):.0f}°]"
                              f"  heading={math.degrees(h):.0f}°"
                              f"  front_plate=({pos[0]+math.cos(h)*FRONT_OFFSET:.1f},"
                              f"{pos[1]+math.sin(h)*FRONT_OFFSET:.1f})")
                        if i >= 2:
                            break


if __name__ == "__main__":
    main()
