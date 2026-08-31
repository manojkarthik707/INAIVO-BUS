"""
number_plate_controller.py — Persistent 3D Indian License Plate Supervisor.

FIX: Access vehicles via getFromDef("SUMO_VEHICLE0".."SUMO_VEHICLE99") 
rather than scanning children by name field (which holds SUMO trip IDs like "car_0", not DEF names).
"""

import math
from controller import Supervisor

INDIAN_STATES = ["TN", "KA", "MH", "DL", "TS", "GJ", "KL", "AP", "WB", "HR"]
SERIES = ["AB", "CD", "EF", "GH", "JK", "LM", "NP", "QR", "ST", "UV", "WX", "YZ"]

def get_unique_indian_plate(v_idx):
    state = INDIAN_STATES[v_idx % len(INDIAN_STATES)]
    rto = f"{(v_idx * 3 + 1) % 99 + 1:02d}"
    series = SERIES[(v_idx // len(INDIAN_STATES)) % len(SERIES)]
    num = f"{(v_idx * 127 + 1001) % 9000 + 1000:04d}"
    return f"{state} {rto} {series} {num}"

PLATE_D     = 0.012
PLATE_W     = 0.52
PLATE_H     = 0.115
FRONT_DIST  = 2.35
REAR_DIST   = 2.20
PLATE_Z     = 0.42
MAX_VEHICLES = 100
TEXTURE_DIR = "textures/plates"


def plate_vrml(def_name, tex_path):
    return (
        f"DEF {def_name} Solid {{\n"
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
        f"  name \"{def_name.lower()}\"\n"
        f"  locked FALSE\n"
        f"}}\n"
    )


def main():
    robot = Supervisor()
    timestep = int(robot.getBasicTimeStep())
    if timestep <= 0:
        timestep = 32

    root_children = robot.getRoot().getField("children")
    print("[PlateCtrl] Pre-allocating 200 plate Solid nodes at world root...")

    # Pre-allocate all plate nodes
    for i in range(MAX_VEHICLES):
        tex = f"{TEXTURE_DIR}/plate_{i:03d}.png"
        root_children.importMFNodeFromString(-1, plate_vrml(f"PLATE_FRONT_{i}", tex))
        root_children.importMFNodeFromString(-1, plate_vrml(f"PLATE_REAR_{i}",  tex))

    # Cache references to plate nodes
    plate_front = [robot.getFromDef(f"PLATE_FRONT_{i}") for i in range(MAX_VEHICLES)]
    plate_rear  = [robot.getFromDef(f"PLATE_REAR_{i}")  for i in range(MAX_VEHICLES)]
    ok = sum(1 for p in plate_front if p is not None)
    print(f"[PlateCtrl] {ok}/{MAX_VEHICLES} front plate nodes resolved. Ready.")

    # Cache references to SUMO vehicle Solid nodes by DEF name
    # DEF names: SUMO_VEHICLE0 … SUMO_VEHICLE99 (set by sumo_supervisor/Objects.py)
    # Each is a Solid wrapping the vehicle PROTO child.
    # We track slot assignment: SUMO_VEHICLE slot i -> plate slot i (1-to-1, deterministic)
    vehicle_nodes = []
    for i in range(MAX_VEHICLES):
        node = robot.getFromDef(f"SUMO_VEHICLE{i}")
        vehicle_nodes.append(node)

    resolved = sum(1 for v in vehicle_nodes if v is not None)
    print(f"[PlateCtrl] {resolved} SUMO_VEHICLE DEF nodes pre-resolved at startup.")

    # If nodes don't exist yet at startup (vehicles added dynamically), 
    # we'll resolve lazily each step.

    step_count = 0
    while robot.step(timestep) != -1:
        step_count += 1

        # Re-try resolving unresolved vehicle nodes periodically
        if step_count % 30 == 0:
            for i in range(MAX_VEHICLES):
                if vehicle_nodes[i] is None:
                    vehicle_nodes[i] = robot.getFromDef(f"SUMO_VEHICLE{i}")

        for i in range(MAX_VEHICLES):
            v_node = vehicle_nodes[i]
            pf = plate_front[i]
            pr = plate_rear[i]

            if not v_node or not pf or not pr:
                continue

            tf = v_node.getField("translation")
            rf = v_node.getField("rotation")
            if not tf or not rf:
                continue

            pos = tf.getSFVec3f()
            vx, vy, vz = pos

            # Vehicle is hidden/parked far away — park plates too
            if vx > 9000:
                t = pf.getField("translation")
                if t:
                    t.setSFVec3f([10000 + i, i * 5.0, PLATE_Z])
                t = pr.getField("translation")
                if t:
                    t.setSFVec3f([10000 + i, i * 5.0 + 0.5, PLATE_Z])
                continue

            rot = rf.getSFRotation()
            ax, ay, az, angle = rot

            # Webots SUMO vehicles rotate around Z axis
            if az < -0.5:
                heading = -angle
            elif az > 0.5:
                heading = angle
            else:
                heading = 0.0

            fx = math.cos(heading)
            fy = math.sin(heading)

            # Front plate
            pft = pf.getField("translation")
            pfr = pf.getField("rotation")
            if pft:
                pft.setSFVec3f([vx + fx * FRONT_DIST, vy + fy * FRONT_DIST, PLATE_Z])
            if pfr:
                pfr.setSFRotation([0, 0, 1, heading])

            # Rear plate
            prt = pr.getField("translation")
            prr = pr.getField("rotation")
            if prt:
                prt.setSFVec3f([vx - fx * REAR_DIST, vy - fy * REAR_DIST, PLATE_Z])
            if prr:
                prr.setSFRotation([0, 0, 1, heading + math.pi])


if __name__ == "__main__":
    main()
