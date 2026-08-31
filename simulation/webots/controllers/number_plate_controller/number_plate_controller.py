"""
number_plate_controller.py — Optimized 3D Indian License Plate Supervisor.

FIXES:
  1. Velocity-vector heading (correct regardless of rotation field encoding quirks).
  2. Plate Z tracks vehicle Z exactly.
  3. FRONT/REAR offsets tuned empirically for bumper placement.
  4. Override default white blank plates by setting the frontLicensePlate / rearLicensePlate
     fields on the PROTO child if they exist, else the blank plate is just overlaid.
  5. Pose nodes (no physics overhead).
  6. All field refs cached at startup.
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

# Plate geometry (Box in Webots XYZ where Z=up)
# size: thin-dim(X=depth along heading), width(Y=lateral), height(Z=vertical)
PLATE_DEPTH  = 0.028   # X: depth (faces heading direction)
PLATE_WIDTH  = 1.04    # Y: horizontal width  (2x real size, visible at distance)
PLATE_HEIGHT = 0.230   # Z: vertical height   (2x real size)

# Offsets from vehicle Solid center along heading direction
FRONT_DIST =  2.20    # m ahead of Solid center (tuned for bmwx5 / typical sedan)
REAR_DIST  =  2.05    # m behind Solid center

PLATE_Z_ABOVE_VEH = -0.02  # plate Z = vz + this (slightly below veh center = bumper level)

MAX_VEH      = 100
TEX_DIR      = "textures/plates"
UPDATE_EVERY = 1   # update every step (fields cached, cheap)


def plate_vrml(def_name, tex_path):
    """Pose node — zero physics overhead."""
    return (
        f"DEF {def_name} Pose {{\n"
        f"  translation 10000 0 0.4\n"
        f"  rotation 0 0 1 0\n"
        f"  children [\n"
        f"    Shape {{\n"
        f"      appearance PBRAppearance {{\n"
        f"        baseColorMap ImageTexture {{\n"
        f"          url [ \"{tex_path}\" ]\n"
        f"        }}\n"
        f"        roughness 0.35\n"
        f"        metalness 0.0\n"
        f"        emissiveColor 0.05 0.05 0.05\n"
        f"      }}\n"
        f"      geometry Box {{\n"
        f"        size {PLATE_DEPTH} {PLATE_WIDTH} {PLATE_HEIGHT}\n"
        f"      }}\n"
        f"    }}\n"
        f"  ]\n"
        f"}}\n"
    )


def main():
    robot    = Supervisor()
    timestep = int(robot.getBasicTimeStep()) or 32

    root_ch = robot.getRoot().getField("children")
    print("[PlateCtrl] Injecting 200 Pose plate nodes (no physics)...")
    for i in range(MAX_VEH):
        tex = f"{TEX_DIR}/plate_{i:03d}.png"
        root_ch.importMFNodeFromString(-1, plate_vrml(f"PLATE_F_{i}", tex))
        root_ch.importMFNodeFromString(-1, plate_vrml(f"PLATE_R_{i}", tex))

    # ── Cache plate field refs ────────────────────────────────────────────────
    pf_trans, pf_rot, pr_trans, pr_rot = [], [], [], []
    for i in range(MAX_VEH):
        fn = robot.getFromDef(f"PLATE_F_{i}")
        rn = robot.getFromDef(f"PLATE_R_{i}")
        pf_trans.append(fn.getField("translation") if fn else None)
        pf_rot.append(  fn.getField("rotation")    if fn else None)
        pr_trans.append(rn.getField("translation") if rn else None)
        pr_rot.append(  rn.getField("rotation")    if rn else None)

    # ── Cache vehicle field refs ──────────────────────────────────────────────
    veh_trans = [None] * MAX_VEH

    def resolve_vehicles():
        for i in range(MAX_VEH):
            if veh_trans[i] is None:
                nd = robot.getFromDef(f"SUMO_VEHICLE{i}")
                if nd:
                    veh_trans[i] = nd.getField("translation")
                    # Try to remove default blank plate text if PROTO exposes it
                    ch_f = nd.getField("children")
                    if ch_f and ch_f.getCount() > 0:
                        proto = ch_f.getMFNode(0)
                        if proto:
                            for field_name in ["frontLicensePlate", "rearLicensePlate",
                                               "licensePlate", "plateText"]:
                                f = proto.getField(field_name)
                                if f:
                                    try:
                                        f.setSFString(" ")  # blank out default plate
                                    except Exception:
                                        pass

    resolve_vehicles()
    resolved = sum(1 for t in veh_trans if t)
    print(f"[PlateCtrl] {resolved}/{MAX_VEH} vehicle nodes cached. Running.")

    # ── Velocity-based heading tracker ────────────────────────────────────────
    prev_xy   = [None] * MAX_VEH   # (x, y) from last step
    heading   = [0.0] * MAX_VEH   # last known heading (radians, 0=East, π/2=North)

    step = 0
    while robot.step(timestep) != -1:
        step += 1

        if step % 60 == 0:
            resolve_vehicles()

        for i in range(MAX_VEH):
            vt = veh_trans[i]
            if not vt:
                continue

            pos = vt.getSFVec3f()
            vx, vy, vz = pos

            # Park plates for hidden vehicles
            if vx > 9000:
                t = pf_trans[i]
                if t: t.setSFVec3f([10001 + i, 0.0, 0.4])
                t = pr_trans[i]
                if t: t.setSFVec3f([10001 + i, 0.5, 0.4])
                prev_xy[i] = None
                continue

            # ── Velocity-vector heading (coordinate-system agnostic) ──────────
            cur = (vx, vy)
            if prev_xy[i] is not None:
                ox, oy = prev_xy[i]
                dx, dy = vx - ox, vy - oy
                dist = math.hypot(dx, dy)
                if dist > 0.003:          # moving — update heading
                    heading[i] = math.atan2(dy, dx)
            prev_xy[i] = cur

            h  = heading[i]
            fx = math.cos(h)
            fy = math.sin(h)
            pz = vz + PLATE_Z_ABOVE_VEH

            # Front plate
            pft = pf_trans[i]
            pfr = pf_rot[i]
            if pft:
                pft.setSFVec3f([vx + fx * FRONT_DIST,
                                vy + fy * FRONT_DIST,
                                pz])
            if pfr:
                pfr.setSFRotation([0, 0, 1, h])

            # Rear plate (facing opposite direction)
            prt = pr_trans[i]
            prr = pr_rot[i]
            if prt:
                prt.setSFVec3f([vx - fx * REAR_DIST,
                                vy - fy * REAR_DIST,
                                pz])
            if prr:
                prr.setSFRotation([0, 0, 1, h + math.pi])


if __name__ == "__main__":
    main()
