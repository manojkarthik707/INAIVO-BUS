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

PLATE_DEPTH  = 0.030
PLATE_WIDTH  = 1.04
PLATE_HEIGHT = 0.230

DEFAULT_FRONT_OFFSET =  2.15
DEFAULT_REAR_OFFSET  = -2.05
PLATE_Z_OFFSET       = -0.05

MAX_VEH   = 20
TEX_DIR   = "textures/plates"
CONFIG_FILE = "plate_offsets.json"
PARKED_X  = 10500.0

def plate_vrml(def_name, tex_path):
    return (
        f"DEF {def_name} Solid {{\n"
        f"  translation {PARKED_X} 0 0.4\n"
        f"  rotation 0 0 1 0\n"
        f"  children [\n"
        f"    DEF {def_name}_SCALE Transform {{\n"
        f"      scale 1 1 1\n"
        f"      children [\n"
        f"        Shape {{\n"
        f"          appearance PBRAppearance {{\n"
        f"            baseColorMap ImageTexture {{\n"
        f"              url [ \"{tex_path}\" ]\n"
        f"            }}\n"
        f"            roughness 0.3\n"
        f"            metalness 0.0\n"
        f"          }}\n"
        f"          geometry Box {{\n"
        f"            size {PLATE_DEPTH} {PLATE_WIDTH} {PLATE_HEIGHT}\n"
        f"          }}\n"
        f"        }}\n"
        f"      ]\n"
        f"    }}\n"
        f"  ]\n"
        f"  boundingObject Box {{\n"
        f"    size {PLATE_DEPTH} {PLATE_WIDTH} {PLATE_HEIGHT}\n"
        f"  }}\n"
        f"}}\n"
    )

def apply_3d_rotation(v_local, rot):
    """Apply an axis-angle rotation to a local 3D vector using Rodrigues' rotation formula."""
    ax, ay, az, angle = rot
    c = math.cos(angle)
    s = math.sin(angle)
    C = 1 - c
    
    m00 = ax*ax*C + c
    m01 = ax*ay*C - az*s
    m02 = ax*az*C + ay*s
    
    m10 = ay*ax*C + az*s
    m11 = ay*ay*C + c
    m12 = ay*az*C - ax*s
    
    m20 = az*ax*C - ay*s
    m21 = az*ay*C + ax*s
    m22 = az*az*C + c
    
    x = m00*v_local[0] + m01*v_local[1] + m02*v_local[2]
    y = m10*v_local[0] + m11*v_local[1] + m12*v_local[2]
    z = m20*v_local[0] + m21*v_local[1] + m22*v_local[2]
    
    return [x, y, z]

def compose_rotations_z(rot_base, extra_yaw):
    """Add extra_yaw (radians) to the base axis-angle rotation."""
    ax, ay, az, angle = rot_base
    if abs(az) < 0.5:
        return rot_base
    new_angle = (angle + extra_yaw) if az > 0 else (angle - extra_yaw)
    return [ax, ay, az, new_angle]

def main():
    robot    = Supervisor()
    timestep = int(robot.getBasicTimeStep()) or 32

    # Inject standalone plates into the ROOT of the scene
    root_ch = robot.getRoot().getField("children")
    for i in range(MAX_VEH):
        tex = f"{TEX_DIR}/plate_{i:03d}.png"
        root_ch.importMFNodeFromString(-1, plate_vrml(f"PLATE_F_{i}", tex))
        root_ch.importMFNodeFromString(-1, plate_vrml(f"PLATE_R_{i}", tex))

    pf_trans, pf_rot, pf_scale = [], [], []
    pr_trans, pr_rot, pr_scale = [], [], []
    for i in range(MAX_VEH):
        fn = robot.getFromDef(f"PLATE_F_{i}")
        rn = robot.getFromDef(f"PLATE_R_{i}")
        fs = robot.getFromDef(f"PLATE_F_{i}_SCALE")
        rs = robot.getFromDef(f"PLATE_R_{i}_SCALE")
        
        pf_trans.append(fn.getField("translation") if fn else None)
        pf_rot.append(  fn.getField("rotation")    if fn else None)
        pf_scale.append(fs.getField("scale")       if fs else None)
        
        pr_trans.append(rn.getField("translation") if rn else None)
        pr_rot.append(  rn.getField("rotation")    if rn else None)
        pr_scale.append(rs.getField("scale")       if rs else None)

    veh_trans      = [None] * MAX_VEH
    veh_rot        = [None] * MAX_VEH
    proto_trans    = [None] * MAX_VEH
    veh_front_offs = [DEFAULT_FRONT_OFFSET] * MAX_VEH
    veh_rear_offs  = [DEFAULT_REAR_OFFSET]  * MAX_VEH
    veh_front_z_offs = [PLATE_Z_OFFSET]     * MAX_VEH
    veh_rear_z_offs  = [PLATE_Z_OFFSET]     * MAX_VEH
    veh_scales       = [1.0]                * MAX_VEH
    veh_type_names = [""] * MAX_VEH

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
            nd = robot.getFromDef(f"SUMO_VEHICLE{i}")
            if nd:
                veh_trans[i] = nd.getField("translation")
                veh_rot[i]   = nd.getField("rotation")
                type_name = nd.getTypeName().lower()
                veh_type_names[i] = type_name
                
                # Check if it has an internal chassis offset
                ch_f = nd.getField("children")
                if ch_f and ch_f.getCount() > 0:
                    child = ch_f.getMFNode(0)
                    if child:
                        pt_field = child.getField("translation")
                        if pt_field:
                            proto_trans[i] = pt_field

                if type_name not in type_configs:
                    config_changed = True
                    if "motor" in type_name or "bike" in type_name:
                        type_configs[type_name] = {"front": 1.05, "rear": -1.00, "front_z": 0.10, "rear_z": 0.10, "scale": 0.6}
                    elif "scoot" in type_name or "moped" in type_name:
                        type_configs[type_name] = {"front": 0.95, "rear": -0.90, "front_z": 0.08, "rear_z": 0.08, "scale": 0.5}
                    elif "bus" in type_name:
                        type_configs[type_name] = {"front": 5.10, "rear": -4.90, "front_z": -0.10, "rear_z": -0.10, "scale": 1.3}
                    elif "sprinter" in type_name or "van" in type_name:
                        type_configs[type_name] = {"front": 2.85, "rear": -2.75, "front_z": -0.05, "rear_z": -0.05, "scale": 1.1}
                    else:
                        type_configs[type_name] = {"front": 2.15, "rear": -2.05, "front_z": -0.05, "rear_z": -0.05, "scale": 1.0}

                # Clear built-in plates
                for fname in ["frontLicensePlate", "rearLicensePlate", "licensePlate", "plateText"]:
                    f2 = nd.getField(fname)
                    if f2:
                        try: f2.setSFString(" ")
                        except: pass
            else:
                veh_trans[i] = None
                veh_rot[i] = None
                proto_trans[i] = None

            if veh_type_names[i] in type_configs:
                cfg = type_configs[veh_type_names[i]]
                veh_front_offs[i] = cfg.get("front", DEFAULT_FRONT_OFFSET)
                veh_rear_offs[i]  = cfg.get("rear", DEFAULT_REAR_OFFSET)
                veh_front_z_offs[i] = cfg.get("front_z", cfg.get("z", PLATE_Z_OFFSET))
                veh_rear_z_offs[i]  = cfg.get("rear_z", cfg.get("z", PLATE_Z_OFFSET))
                veh_scales[i]       = cfg.get("scale", 1.0)

        if config_changed:
            save_config()

    print("[PlateCtrl] Perfect 3D Pitch/Roll Tracking Mode Online.")
    resolve_vehicles()

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
            if pos[0] > 9000:
                if pf_trans[i]: pf_trans[i].setSFVec3f([PARKED_X + i, 0, 0.4])
                if pr_trans[i]: pr_trans[i].setSFVec3f([PARKED_X + i, 0.5, 0.4])
                continue

            rot = vr.getSFRotation()
            
            chassis_y = 0.0
            if proto_trans[i]:
                chassis_y = proto_trans[i].getSFVec3f()[1]

            # True 3D vectors accounting for pitch/roll/yaw
            f_local = [veh_front_offs[i], chassis_y, veh_front_z_offs[i]]
            r_local = [veh_rear_offs[i],  chassis_y, veh_rear_z_offs[i]]
            
            f_world_offset = apply_3d_rotation(f_local, rot)
            r_world_offset = apply_3d_rotation(r_local, rot)

            # Apply exact world position
            if pf_trans[i]: 
                pf_trans[i].setSFVec3f([pos[0] + f_world_offset[0], pos[1] + f_world_offset[1], pos[2] + f_world_offset[2]])
            if pr_trans[i]: 
                pr_trans[i].setSFVec3f([pos[0] + r_world_offset[0], pos[1] + r_world_offset[1], pos[2] + r_world_offset[2]])
                
            # Apply exact 3D orientation
            if pf_rot[i]:
                pf_rot[i].setSFRotation(rot)
            if pr_rot[i]:
                pr_rot[i].setSFRotation(compose_rotations_z(rot, math.pi))
                
            # Apply dynamic scale
            if pf_scale[i]:
                s = veh_scales[i]
                pf_scale[i].setSFVec3f([s, s, s])
            if pr_scale[i]:
                s = veh_scales[i]
                pr_scale[i].setSFVec3f([s, s, s])

if __name__ == "__main__":
    main()
