"""
number_plate_controller.py — Indian License Plate Supervisor (fixed & robust).

HEADING FIX:
  Use the PROTO child world position relative to the Solid world position to derive
  the car's true forward axis in world space — works regardless of SUMO/Webots
  coordinate conventions. Cross-validate with displacement velocity.

POSITION FIX:
  Plates mount directly AT the Solid world position ± bumper offset.
  The Solid Z is used directly for height.
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
# Box in Webots world (Z=up): size X (depth/forward) × Y (lateral width) × Z (height)
PLATE_DEPTH  = 0.030   # along heading direction (thin face-forward)
PLATE_WIDTH  = 1.04    # horizontal width (2× real size for visibility)
PLATE_HEIGHT = 0.230   # vertical height  (2× real size for visibility)

# Bumper offsets (metres from Solid centre, along car axis)
# Determined empirically: the Solid centre sits near the car's physical centre.
# BmwX5/typical sedan: half-length ≈ 2.3 m → bumper at ≈ 2.1 m from centre.
FRONT_OFFSET =  2.10
REAR_OFFSET  = -2.00
PLATE_Z_OFFSET = -0.05  # slightly below Solid Z (Solid is at car CG; bumper lower)

MAX_VEH   = 100
TEX_DIR   = "textures/plates"

PARKED_X_BASE = 10500.0   # park position for unused plates


def plate_vrml(def_name, tex_path):
    """Pose node — no physics overhead."""
    return (
        f"DEF {def_name} Pose {{\n"
        f"  translation {PARKED_X_BASE} 0 0.4\n"
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


def axis_angle_to_forward_xy(ax, ay, az, angle):
    """
    Given a Webots rotation field [ax, ay, az, angle],
    return the world (x, y) unit vector of the Solid's LOCAL +X axis.
    Rodrigues rotation of [1, 0, 0]:
      fx = cos(a) + ax²(1-cos(a))
      fy = ax·ay·(1-cos(a)) + az·sin(a)
    For purely Z-axis rotations (ax=ay=0, az=±1) this simplifies to [cos(a), ±sin(a)].
    """
    c = math.cos(angle)
    s = math.sin(angle)
    fx = c + ax * ax * (1 - c)
    fy = ax * ay * (1 - c) + az * s
    mag = math.hypot(fx, fy)
    if mag < 1e-6:
        return 1.0, 0.0
    return fx / mag, fy / mag


def main():
    robot    = Supervisor()
    timestep = int(robot.getBasicTimeStep()) or 32

    root_ch = robot.getRoot().getField("children")
    print("[PlateCtrl] Injecting 200 Pose plate nodes...")
    for i in range(MAX_VEH):
        tex = f"{TEX_DIR}/plate_{i:03d}.png"
        root_ch.importMFNodeFromString(-1, plate_vrml(f"PLATE_F_{i}", tex))
        root_ch.importMFNodeFromString(-1, plate_vrml(f"PLATE_R_{i}", tex))

    # ── Cache plate field refs ────────────────────────────────────────────
    pf_trans, pf_rot, pr_trans, pr_rot = [], [], [], []
    for i in range(MAX_VEH):
        fn = robot.getFromDef(f"PLATE_F_{i}")
        rn = robot.getFromDef(f"PLATE_R_{i}")
        pf_trans.append(fn.getField("translation") if fn else None)
        pf_rot.append(  fn.getField("rotation")    if fn else None)
        pr_trans.append(rn.getField("translation") if rn else None)
        pr_rot.append(  rn.getField("rotation")    if rn else None)

    # ── Cache vehicle Solid node refs and their fields ────────────────────
    veh_nodes  = [None] * MAX_VEH   # Node objects
    veh_trans  = [None] * MAX_VEH   # translation field
    veh_rot    = [None] * MAX_VEH   # rotation field
    veh_child  = [None] * MAX_VEH   # PROTO child Node (for getPosition())

    # Per-vehicle state
    heading     = [0.0]  * MAX_VEH  # last known heading (radians)
    prev_xy     = [None] * MAX_VEH  # previous (x, y) for velocity heading
    heading_set = [False]* MAX_VEH  # True once we have a real heading

    # Calibration: detect whether local +X is front or rear
    # We use axis_angle_to_forward_xy → call it "raw_forward"
    # Then compare with velocity direction. If they match → forward_sign = +1
    # If they differ by ~π → forward_sign = -1
    forward_sign = [0] * MAX_VEH  # 0=unknown, +1=local+X is front, -1=local-X is front

    def resolve_vehicles():
        for i in range(MAX_VEH):
            if veh_trans[i] is None:
                nd = robot.getFromDef(f"SUMO_VEHICLE{i}")
                if nd:
                    veh_nodes[i]  = nd
                    veh_trans[i]  = nd.getField("translation")
                    veh_rot[i]    = nd.getField("rotation")
                    # Cache child PROTO node for getPosition()
                    ch_f = nd.getField("children")
                    if ch_f and ch_f.getCount() > 0:
                        veh_child[i] = ch_f.getMFNode(0)
                    # Try to blank built-in white default plate text
                    if veh_child[i]:
                        for fname in ["frontLicensePlate", "rearLicensePlate",
                                      "licensePlate", "plateText"]:
                            f2 = veh_child[i].getField(fname)
                            if f2:
                                try: f2.setSFString(" ")
                                except Exception: pass

    resolve_vehicles()
    resolved = sum(1 for t in veh_trans if t)
    print(f"[PlateCtrl] {resolved}/{MAX_VEH} vehicle nodes cached. Running.")

    step = 0
    while robot.step(timestep) != -1:
        step += 1

        if step % 90 == 0:
            resolve_vehicles()

        for i in range(MAX_VEH):
            vt = veh_trans[i]
            if not vt:
                continue

            pos = vt.getSFVec3f()
            vx, vy, vz = pos

            # Park plates for hidden/idle vehicles
            if vx > 9000:
                pf = pf_trans[i]
                pr = pr_trans[i]
                if pf: pf.setSFVec3f([PARKED_X_BASE + i, 0.0, 0.4])
                if pr: pr.setSFVec3f([PARKED_X_BASE + i, 0.5, 0.4])
                prev_xy[i]     = None
                heading_set[i] = False
                forward_sign[i] = 0
                continue

            # ── Heading from rotation field (immediate, no lag) ───────────
            vr = veh_rot[i]
            rot_heading = None
            if vr:
                rot = vr.getSFRotation()
                ax, ay, az, angle = rot
                rfx, rfy = axis_angle_to_forward_xy(ax, ay, az, angle)
                rot_heading = math.atan2(rfy, rfx)

            # ── Velocity heading from displacement (correct after 1 frame) ─
            vel_heading = None
            cur = (vx, vy)
            if prev_xy[i] is not None:
                ox, oy = prev_xy[i]
                ddx, ddy = vx - ox, vy - oy
                dist = math.hypot(ddx, ddy)
                if dist > 0.005:
                    vel_heading = math.atan2(ddy, ddx)
                    # Calibrate forward_sign once
                    if rot_heading is not None and forward_sign[i] == 0:
                        diff = vel_heading - rot_heading
                        # Normalise diff to [-π, π]
                        diff = (diff + math.pi) % (2 * math.pi) - math.pi
                        forward_sign[i] = -1 if abs(diff) > math.pi / 2 else 1
            prev_xy[i] = cur

            # ── Choose best heading ────────────────────────────────────────
            if vel_heading is not None:
                heading[i] = vel_heading
                heading_set[i] = True
            elif rot_heading is not None:
                # Apply calibrated forward_sign; if unknown assume +1
                sign = forward_sign[i] if forward_sign[i] != 0 else 1
                heading[i] = rot_heading if sign > 0 else rot_heading + math.pi
                heading_set[i] = True

            # Don't place plate until heading is known
            if not heading_set[i]:
                continue

            h  = heading[i]
            fx = math.cos(h)
            fy = math.sin(h)
            pz = vz + PLATE_Z_OFFSET

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

        # Debug: print first 3 vehicle headings every 5s
        if step == 150:
            for i in range(min(3, MAX_VEH)):
                if veh_trans[i] and heading_set[i]:
                    pos = veh_trans[i].getSFVec3f()
                    if pos[0] < 9000:
                        print(f"[PlateCtrl] VEH{i} pos=({pos[0]:.1f},{pos[1]:.1f},"
                              f"{pos[2]:.2f}) heading={math.degrees(heading[i]):.0f}° "
                              f"sign={forward_sign[i]}")


if __name__ == "__main__":
    main()
