"""
number_plate_controller.py — Persistent 3D Indian License Plate Supervisor.

Approach:
- Creates front and rear license plate Solid nodes ONCE at startup for each vehicle slot.
- Every timestep, reads the vehicle's translation+rotation and places front/rear plates
  at the correct bumper offsets in world space.
- Plates are always visible and follow the vehicle exactly, independent of SUMO overrides.
"""

import math
from controller import Supervisor, Field

INDIAN_STATES = ["TN", "KA", "MH", "DL", "TS", "GJ", "KL", "AP", "WB", "HR"]
SERIES = ["AB", "CD", "EF", "GH", "JK", "LM", "NP", "QR", "ST", "UV", "WX", "YZ"]

def get_unique_indian_plate(v_idx):
    state = INDIAN_STATES[v_idx % len(INDIAN_STATES)]
    rto = f"{(v_idx * 3 + 1) % 99 + 1:02d}"
    series = SERIES[(v_idx // len(INDIAN_STATES)) % len(SERIES)]
    num = f"{(v_idx * 127 + 1001) % 9000 + 1000:04d}"
    return f"{state} {rto} {series} {num}"

# Plate dimensions and offsets
FRONT_OFFSET = 2.3    # metres ahead of vehicle center
REAR_OFFSET  = -2.1   # metres behind vehicle center
PLATE_HEIGHT_Z = 0.42  # metres above ground

MAX_VEHICLES = 100

def plate_vrml(def_name, plate_str):
    return (
        f"DEF {def_name} Solid {{\n"
        f"  translation 10000 0 {PLATE_HEIGHT_Z}\n"
        f"  rotation 0 0 1 0\n"
        f"  children [\n"
        f"    Shape {{\n"
        f"      appearance PBRAppearance {{\n"
        f"        baseColor 0.95 0.95 0.90\n"
        f"        roughness 0.3\n"
        f"        metalness 0.0\n"
        f"      }}\n"
        f"      geometry Box {{ size 0.022 0.50 0.115 }}\n"
        f"    }}\n"
        f"    Pose {{\n"
        f"      translation 0.015 0.0 0.0\n"
        f"      rotation 0 1 0 1.5708\n"
        f"      children [\n"
        f"        Shape {{\n"
        f"          appearance PBRAppearance {{\n"
        f"            baseColor 0.05 0.05 0.05\n"
        f"            roughness 0.1\n"
        f"            metalness 0.0\n"
        f"          }}\n"
        f"          geometry Text {{\n"
        f"            string [ \"{plate_str}\" ]\n"
        f"            fontStyle FontStyle {{\n"
        f"              size 0.060\n"
        f"              family \"Arial\"\n"
        f"              style \"BOLD\"\n"
        f"            }}\n"
        f"          }}\n"
        f"        }}\n"
        f"      ]\n"
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
    print("Number Plate Supervisor Online. Mounting 3D Indian License Plates on all vehicles.")

    plate_nodes = {}      # vehicle_name -> {'front': node, 'rear': node, 'plate': str, 'idx': int}
    spawned = set()

    # Pre-allocate 100 front and 100 rear plates (hidden at 10000 x) 
    print("Pre-allocating 100 plate pairs...")
    for i in range(MAX_VEHICLES):
        plate_str = get_unique_indian_plate(i)
        front_def = f"PLATE_FRONT_{i}"
        rear_def  = f"PLATE_REAR_{i}"
        root_children.importMFNodeFromString(-1, plate_vrml(front_def, plate_str))
        root_children.importMFNodeFromString(-1, plate_vrml(rear_def, plate_str))

    # Get references to all pre-allocated plate nodes
    plate_front_nodes = []
    plate_rear_nodes  = []
    for i in range(MAX_VEHICLES):
        pf = robot.getFromDef(f"PLATE_FRONT_{i}")
        pr = robot.getFromDef(f"PLATE_REAR_{i}")
        plate_front_nodes.append(pf)
        plate_rear_nodes.append(pr)
    print(f"Pre-allocated {MAX_VEHICLES} front + {MAX_VEHICLES} rear plates in world.")

    # Pool of free slot indices
    free_slots = list(range(MAX_VEHICLES))
    vehicle_slots = {}   # vehicle_name -> slot_index

    while robot.step(timestep) != -1:
        n_children = root_children.getCount()

        active_names = set()

        for i in range(n_children):
            node = root_children.getMFNode(i)
            if not node:
                continue
            name_field = node.getField("name")
            if not name_field:
                continue
            name = name_field.getSFString()
            if "SUMO_VEHICLE" not in name:
                continue

            t_field = node.getField("translation")
            r_field = node.getField("rotation")
            if not t_field or not r_field:
                continue

            pos = t_field.getSFVec3f()
            rot = r_field.getSFRotation()

            # Skip hidden vehicles (parked far away at x=10000)
            if pos[0] > 9000:
                continue

            active_names.add(name)

            # Assign a free plate slot if new vehicle
            if name not in vehicle_slots:
                if free_slots:
                    slot = free_slots.pop(0)
                    vehicle_slots[name] = slot
                else:
                    continue

            slot = vehicle_slots[name]
            pf_node = plate_front_nodes[slot]
            pr_node = plate_rear_nodes[slot]
            if not pf_node or not pr_node:
                continue

            # Compute vehicle heading angle
            if abs(rot[2]) > 0.5:
                angle = rot[3] if rot[2] > 0 else -rot[3]
            else:
                angle = 0.0

            # Forward unit vector
            fx = math.cos(angle)
            fy = math.sin(angle)

            vx, vy, vz = pos
            # Position front plate
            front_x = vx + fx * FRONT_OFFSET
            front_y = vy + fy * FRONT_OFFSET
            pf_t = pf_node.getField("translation")
            pf_r = pf_node.getField("rotation")
            if pf_t and pf_r:
                pf_t.setSFVec3f([front_x, front_y, PLATE_HEIGHT_Z])
                pf_r.setSFRotation([0, 0, 1, angle])

            # Position rear plate
            rear_x = vx + fx * REAR_OFFSET
            rear_y = vy + fy * REAR_OFFSET
            pr_t = pr_node.getField("translation")
            pr_r = pr_node.getField("rotation")
            if pr_t and pr_r:
                pr_t.setSFVec3f([rear_x, rear_y, PLATE_HEIGHT_Z])
                pr_r.setSFRotation([0, 0, 1, angle + math.pi])

        # Return slots for vehicles that have gone hidden / disappeared
        for name, slot in list(vehicle_slots.items()):
            if name not in active_names:
                pf_node = plate_front_nodes[slot]
                pr_node = plate_rear_nodes[slot]
                if pf_node:
                    pf_t = pf_node.getField("translation")
                    if pf_t:
                        pf_t.setSFVec3f([10000, slot * 5, PLATE_HEIGHT_Z])
                if pr_node:
                    pr_t = pr_node.getField("translation")
                    if pr_t:
                        pr_t.setSFVec3f([10000, slot * 5 + 200, PLATE_HEIGHT_Z])
                free_slots.append(slot)
                del vehicle_slots[name]

if __name__ == "__main__":
    main()
