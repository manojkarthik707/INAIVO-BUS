"""
number_plate_controller.py — Persistent 3D Indian License Plate Supervisor.

Strategy:
- Pre-allocates 200 Solid nodes (100 front + 100 rear) IN THE WORLD at startup.
- Each plate is a flat Box with the plate PNG as an ImageTexture (no PROTO needed).
- Every timestep, reads each active SUMO vehicle's position/rotation
  and teleports the matching plate pair to the front/rear bumper.
"""

import math
import os
from controller import Supervisor

INDIAN_STATES = ["TN", "KA", "MH", "DL", "TS", "GJ", "KL", "AP", "WB", "HR"]
SERIES = ["AB", "CD", "EF", "GH", "JK", "LM", "NP", "QR", "ST", "UV", "WX", "YZ"]

def get_unique_indian_plate(v_idx):
    state = INDIAN_STATES[v_idx % len(INDIAN_STATES)]
    rto = f"{(v_idx * 3 + 1) % 99 + 1:02d}"
    series = SERIES[(v_idx // len(INDIAN_STATES)) % len(SERIES)]
    num = f"{(v_idx * 127 + 1001) % 9000 + 1000:04d}"
    return f"{state} {rto} {series} {num}"

# Plate physical dimensions (in Webots metres)
PLATE_W     = 0.52   # width  (x-axis of the plate)
PLATE_H     = 0.115  # height (y-axis of the plate) 
PLATE_D     = 0.012  # depth  (thin slab)
FRONT_DIST  = 2.35   # metres ahead of vehicle origin
REAR_DIST   = 2.20   # metres behind vehicle origin
PLATE_Z     = 0.42   # height above ground

MAX_VEHICLES = 100

# Path to pre-generated plate textures (relative path works for Webots ImageTexture)
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
    print("Number Plate Supervisor: Pre-allocating 200 plate Solid nodes...")

    # Pre-allocate all plate nodes at startup
    for i in range(MAX_VEHICLES):
        tex_path = f"{TEXTURE_DIR}/plate_{i:03d}.png"
        root_children.importMFNodeFromString(-1, plate_vrml(f"PLATE_FRONT_{i}", tex_path))
        root_children.importMFNodeFromString(-1, plate_vrml(f"PLATE_REAR_{i}",  tex_path))

    print("Building node reference cache...")
    plate_front = []
    plate_rear  = []
    for i in range(MAX_VEHICLES):
        pf = robot.getFromDef(f"PLATE_FRONT_{i}")
        pr = robot.getFromDef(f"PLATE_REAR_{i}")
        plate_front.append(pf)
        plate_rear.append(pr)

    free_slots   = list(range(MAX_VEHICLES))
    vehicle_slots = {}   # vehicle_name -> slot_index

    print("Number Plate Supervisor: Ready. Tracking vehicles...")

    while robot.step(timestep) != -1:
        n_children = root_children.getCount()
        active_names = set()

        for i in range(n_children):
            node = root_children.getMFNode(i)
            if not node:
                continue
            nf = node.getField("name")
            if not nf:
                continue
            name = nf.getSFString()
            if "SUMO_VEHICLE" not in name:
                continue

            tf = node.getField("translation")
            rf = node.getField("rotation")
            if not tf or not rf:
                continue

            pos = tf.getSFVec3f()
            if pos[0] > 9000:
                continue   # vehicle hidden/parked

            rot = rf.getSFRotation()
            active_names.add(name)

            # Assign slot on first appearance
            if name not in vehicle_slots:
                if not free_slots:
                    continue
                slot = free_slots.pop(0)
                vehicle_slots[name] = slot

            slot = vehicle_slots[name]
            pf_node = plate_front[slot]
            pr_node = plate_rear[slot]

            # Decode heading from rotation field [ax, ay, az, angle]
            # The vehicle rotates around +Z axis, so az should be ±1
            ax, ay, az, angle = rot
            if az < -0.5:
                heading = -angle
            elif az > 0.5:
                heading = angle
            else:
                heading = 0.0

            fx = math.cos(heading)
            fy = math.sin(heading)
            vx, vy, vz = pos

            # Front bumper position
            fx_world = vx + fx * FRONT_DIST
            fy_world = vy + fy * FRONT_DIST
            # Rear bumper position
            rx_world = vx - fx * REAR_DIST
            ry_world = vy - fy * REAR_DIST

            if pf_node:
                pft = pf_node.getField("translation")
                pfr = pf_node.getField("rotation")
                if pft: pft.setSFVec3f([fx_world, fy_world, PLATE_Z])
                if pfr: pfr.setSFRotation([0, 0, 1, heading])

            if pr_node:
                prt = pr_node.getField("translation")
                prr = pr_node.getField("rotation")
                if prt: prt.setSFVec3f([rx_world, ry_world, PLATE_Z])
                if prr: prr.setSFRotation([0, 0, 1, heading + math.pi])

        # Return slots for vanished/hidden vehicles
        for name, slot in list(vehicle_slots.items()):
            if name not in active_names:
                for pn in [plate_front[slot], plate_rear[slot]]:
                    if pn:
                        t = pn.getField("translation")
                        if t:
                            t.setSFVec3f([10000 + slot, slot * 5, PLATE_Z])
                free_slots.append(slot)
                del vehicle_slots[name]


if __name__ == "__main__":
    main()
