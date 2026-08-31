"""
number_plate_controller.py — Optimized 3D Indian License Plate Supervisor.

Performance fixes:
  1. Plate nodes are Pose (no physics) instead of Solid — eliminates 200 physics bodies.
  2. All field refs cached at startup — zero getField() calls in the main loop.
  3. Plate positions updated every 5 steps (~160ms) — plates are decorative, not real-time critical.
  4. Vehicle field refs (translation, rotation) also cached at startup with lazy re-resolve.
"""

import math
from controller import Supervisor

INDIAN_STATES = ["TN", "KA", "MH", "DL", "TS", "GJ", "KL", "AP", "WB", "HR"]
SERIES = ["AB", "CD", "EF", "GH", "JK", "LM", "NP", "QR", "ST", "UV", "WX", "YZ"]

def get_plate(v_idx):
    state = INDIAN_STATES[v_idx % len(INDIAN_STATES)]
    rto   = f"{(v_idx * 3 + 1) % 99 + 1:02d}"
    series = SERIES[(v_idx // len(INDIAN_STATES)) % len(SERIES)]
    num   = f"{(v_idx * 127 + 1001) % 9000 + 1000:04d}"
    return f"{state} {rto} {series} {num}"

PLATE_D    = 0.012
PLATE_W    = 0.52
PLATE_H    = 0.115
FRONT_DIST = 2.35
REAR_DIST  = 2.20
PLATE_Z    = 0.42
MAX_VEH    = 100
TEX_DIR    = "textures/plates"
UPDATE_EVERY = 5   # update plates every N simulation steps


def plate_vrml(def_name, tex_path):
    """Pose node — no physics, no collision, zero engine overhead."""
    return (
        f"DEF {def_name} Pose {{\n"
        f"  translation 10000 0 {PLATE_Z}\n"
        f"  rotation 0 0 1 0\n"
        f"  children [\n"
        f"    Shape {{\n"
        f"      appearance PBRAppearance {{\n"
        f"        baseColorMap ImageTexture {{\n"
        f"          url [ \"{tex_path}\" ]\n"
        f"        }}\n"
        f"        roughness 0.4\n"
        f"        metalness 0.0\n"
        f"      }}\n"
        f"      geometry Box {{ size {PLATE_D} {PLATE_W} {PLATE_H} }}\n"
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

    # ── Cache ALL field references at startup ──────────────────────────────
    # Plate translation/rotation fields
    pf_trans = []   # plate front translation fields
    pf_rot   = []   # plate front rotation fields
    pr_trans = []
    pr_rot   = []

    for i in range(MAX_VEH):
        fn = robot.getFromDef(f"PLATE_F_{i}")
        rn = robot.getFromDef(f"PLATE_R_{i}")
        pf_trans.append(fn.getField("translation") if fn else None)
        pf_rot.append(  fn.getField("rotation")    if fn else None)
        pr_trans.append(rn.getField("translation") if rn else None)
        pr_rot.append(  rn.getField("rotation")    if rn else None)

    # Vehicle translation/rotation fields (from Solid nodes by DEF)
    veh_trans = [None] * MAX_VEH
    veh_rot   = [None] * MAX_VEH

    def resolve_vehicles():
        for i in range(MAX_VEH):
            if veh_trans[i] is None:
                node = robot.getFromDef(f"SUMO_VEHICLE{i}")
                if node:
                    veh_trans[i] = node.getField("translation")
                    veh_rot[i]   = node.getField("rotation")

    resolve_vehicles()
    resolved = sum(1 for t in veh_trans if t)
    print(f"[PlateCtrl] {resolved}/{MAX_VEH} vehicle nodes resolved. "
          f"Updating every {UPDATE_EVERY} steps. Running.")

    HIDDEN = [10001.0, 0.0, PLATE_Z]
    HIDDEN_ROT = [0, 0, 1, 0]
    step = 0

    while robot.step(timestep) != -1:
        step += 1

        # Re-try unresolved vehicle nodes every 60 steps (~2 s)
        if step % 60 == 0:
            resolve_vehicles()

        # Only update plate positions every UPDATE_EVERY steps
        if step % UPDATE_EVERY != 0:
            continue

        for i in range(MAX_VEH):
            pft = pf_trans[i]
            pfr = pf_rot[i]
            prt = pr_trans[i]
            prr = pr_rot[i]
            vt  = veh_trans[i]
            vr  = veh_rot[i]

            if not pft or not vt:
                continue

            pos = vt.getSFVec3f()
            vx, vy, _ = pos

            # Hidden / parked vehicle → park plates off-map
            if vx > 9000:
                pft.setSFVec3f([10001 + i, 0.0, PLATE_Z])
                prt.setSFVec3f([10001 + i, 0.5, PLATE_Z])
                continue

            rot = vr.getSFRotation() if vr else [0, 0, 1, 0]
            ax, ay, az, angle = rot
            heading = angle if az > 0.5 else (-angle if az < -0.5 else 0.0)

            fx = math.cos(heading)
            fy = math.sin(heading)

            # Front plate
            pft.setSFVec3f([vx + fx * FRONT_DIST, vy + fy * FRONT_DIST, PLATE_Z])
            if pfr:
                pfr.setSFRotation([0, 0, 1, heading])

            # Rear plate
            if prt:
                prt.setSFVec3f([vx - fx * REAR_DIST, vy - fy * REAR_DIST, PLATE_Z])
            if prr:
                prr.setSFRotation([0, 0, 1, heading + math.pi])


if __name__ == "__main__":
    main()
