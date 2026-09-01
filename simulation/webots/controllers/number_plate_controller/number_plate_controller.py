"""
number_plate_controller.py — Indian License Plate Supervisor (flawless bumper tracking).

KEY FEATURES:
1. Rotation-field based heading (-yaw) prevents spinning.
2. Vehicle-type tailored bumper offsets (bikes: ±1.0m, cars: ±2.15m, vans: ±2.85m, buses: ±5.10m).
3. Directly tracks vehicle Solid translation (including pothole lane-shifts) with zero drift.
4. 200 Pose nodes (100 Front + 100 Rear) with distinct Indian license plate textures.
"""

import math
import json
import os
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
PLATE_DEPTH  = 0.030
PLATE_WIDTH  = 1.04    # 2x real plate width for high visibility
PLATE_HEIGHT = 0.230   # 2x real plate height

# Default offsets (overridden dynamically per vehicle model)
DEFAULT_FRONT_OFFSET =  2.15
DEFAULT_REAR_OFFSET  = -2.05
PLATE_Z_OFFSET       = -0.05

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


def yaw_from_rotation_field(rot, fallback=0.0):
    """Extract Webots yaw from the rotation field [ax, ay, az, angle]."""
    ax, ay, az, angle = rot
    if abs(az) < 0.5:
        return fallback
    return angle if az > 0 else -angle


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

    veh_trans      = [None] * MAX_VEH
    veh_rot        = [None] * MAX_VEH
    proto_trans    = [None] * MAX_VEH
    veh_front_offs = [DEFAULT_FRONT_OFFSET] * MAX_VEH
    veh_rear_offs  = [DEFAULT_REAR_OFFSET]  * MAX_VEH
    veh_z_offs     = [PLATE_Z_OFFSET]       * MAX_VEH
    veh_type_names = [""] * MAX_VEH
    last_heading   = [0.0] * MAX_VEH

    CONFIG_FILE = "plate_offsets.json"
    type_configs = {}

    def load_config():
        nonlocal type_configs
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    type_configs = json.load(f)
            except: pass

    def save_config():
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(type_configs, f, indent=4)
        except: pass

    def resolve_vehicles():
        load_config()
        config_changed = False

        for i in range(MAX_VEH):
            if veh_trans[i] is None:
                nd = robot.getFromDef(f"SUMO_VEHICLE{i}")
                if nd:
                    veh_trans[i] = nd.getField("translation")
                    veh_rot[i]   = nd.getField("rotation")

                    # Detect vehicle type from child PROTO
                    ch_f = nd.getField("children")
                    if ch_f and ch_f.getCount() > 0:
                        proto = ch_f.getMFNode(0)
                        if proto:
                            pt_field = proto.getField("translation")
                            if pt_field:
                                proto_trans[i] = pt_field

                            type_name = proto.getTypeName().lower()
                            veh_type_names[i] = type_name

                            # Add to config if missing
                            if type_name not in type_configs:
                                config_changed = True
                                if "motor" in type_name or "bike" in type_name:
                                    type_configs[type_name] = {"front": 1.05, "rear": -1.00, "z": 0.10}
                                elif "scoot" in type_name or "moped" in type_name:
                                    type_configs[type_name] = {"front": 0.95, "rear": -0.90, "z": 0.08}
                                elif "bus" in type_name:
                                    type_configs[type_name] = {"front": 5.10, "rear": -4.90, "z": -0.10}
                                elif "sprinter" in type_name or "van" in type_name:
                                    type_configs[type_name] = {"front": 2.85, "rear": -2.75, "z": -0.05}
                                else:
                                    type_configs[type_name] = {"front": 2.15, "rear": -2.05, "z": -0.05}

                            # Blank default PROTO plates
                            for fname in ["frontLicensePlate", "rearLicensePlate",
                                          "licensePlate", "plateText"]:
                                f2 = proto.getField(fname)
                                if f2:
                                    try: f2.setSFString(" ")
                                    except Exception: pass

            # Re-apply offsets from config
            if veh_type_names[i] in type_configs:
                cfg = type_configs[veh_type_names[i]]
                veh_front_offs[i] = cfg.get("front", DEFAULT_FRONT_OFFSET)
                veh_rear_offs[i]  = cfg.get("rear", DEFAULT_REAR_OFFSET)
                veh_z_offs[i]     = cfg.get("z", PLATE_Z_OFFSET)

        if config_changed:
            save_config()

    resolve_vehicles()
    resolved = sum(1 for t in veh_trans if t)
    print(f"[PlateCtrl] {resolved}/{MAX_VEH} nodes cached. Running.")

    step = 0
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

            # Heading from rotation field
            rot = vr.getSFRotation()
            h   = yaw_from_rotation_field(rot, fallback=last_heading[i])
            last_heading[i] = h

            fx  = math.cos(h)
            fy  = math.sin(h)
            nx  = -fy
            ny  = fx
            pz  = vz + veh_z_offs[i]

            f_dist = veh_front_offs[i]
            r_dist = veh_rear_offs[i]

            chassis_y_offset = 0.0
            if proto_trans[i]:
                chassis_y_offset = proto_trans[i].getSFVec3f()[1]

            # Front plate position
            pft = pf_trans[i]
            pfr = pf_rot[i]
            if pft:
                actual = pft.getSFVec3f()
                if actual[0] < 9000:
                    # Visual Tuning Detection
                    dx = actual[0] - vx
                    dy = actual[1] - vy
                    dz = actual[2] - vz
                    user_f_dist = dx * fx + dy * fy
                    
                    # If dragged by > 5cm forward/backward or up/down
                    if abs(user_f_dist - f_dist) > 0.05 or abs(dz - veh_z_offs[i]) > 0.05:
                        veh_front_offs[i] = user_f_dist
                        veh_z_offs[i] = dz
                        f_dist = user_f_dist
                        pz = vz + dz
                        
                        t_name = veh_type_names[i]
                        if t_name in type_configs:
                            type_configs[t_name]["front"] = round(user_f_dist, 3)
                            type_configs[t_name]["z"] = round(dz, 3)
                            save_config()
                            # Instantly propagate to all other vehicles of the same type
                            for k in range(MAX_VEH):
                                if veh_type_names[k] == t_name:
                                    veh_front_offs[k] = user_f_dist
                                    veh_z_offs[k] = dz
                            print(f"[PlateCtrl] UI Tune -> {t_name} FRONT: {user_f_dist:.3f}m, Z: {dz:.3f}m")

                pft.setSFVec3f([vx + fx * f_dist + nx * chassis_y_offset,
                                vy + fy * f_dist + ny * chassis_y_offset,
                                pz])
            if pfr:
                pfr.setSFRotation([0, 0, 1, h])

            # Rear plate position
            prt = pr_trans[i]
            prr = pr_rot[i]
            if prt:
                actual = prt.getSFVec3f()
                if actual[0] < 9000:
                    # Visual Tuning Detection
                    dx = actual[0] - vx
                    dy = actual[1] - vy
                    dz = actual[2] - vz
                    user_r_dist = dx * fx + dy * fy
                    
                    if abs(user_r_dist - r_dist) > 0.05 or abs(dz - veh_z_offs[i]) > 0.05:
                        veh_rear_offs[i] = user_r_dist
                        veh_z_offs[i] = dz
                        r_dist = user_r_dist
                        pz = vz + dz
                        
                        t_name = veh_type_names[i]
                        if t_name in type_configs:
                            type_configs[t_name]["rear"] = round(user_r_dist, 3)
                            type_configs[t_name]["z"] = round(dz, 3)
                            save_config()
                            # Instantly propagate to all other vehicles of the same type
                            for k in range(MAX_VEH):
                                if veh_type_names[k] == t_name:
                                    veh_rear_offs[k] = user_r_dist
                                    veh_z_offs[k] = dz
                            print(f"[PlateCtrl] UI Tune -> {t_name} REAR: {user_r_dist:.3f}m, Z: {dz:.3f}m")

                prt.setSFVec3f([vx + fx * r_dist + nx * chassis_y_offset,
                                vy + fy * r_dist + ny * chassis_y_offset,
                                pz])
            if prr:
                prr.setSFRotation([0, 0, 1, h + math.pi])


if __name__ == "__main__":
    main()
