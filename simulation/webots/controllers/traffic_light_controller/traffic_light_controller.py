"""
traffic_light_controller.py — Synchronized Indian Free Left Traffic Signal Controller.

Indian Left-Hand Drive Traffic Rules:
1. Free Left Turn:
   - Green Left Arrow is PERPETUALLY ILLUMINATED (100% Free Left).
   - Left-turning vehicles in Lane 0 proceed continuously.
2. Through & Right Turns:
   - Synchronized dynamically with SUMO's Actuated Traffic Lights via tls_switch.xml.
"""

import sys
import os
import re
from controller import Supervisor

def set_mat(mat_node, on_color):
    if mat_node:
        mat_node.getField("emissiveColor").setSFColor(on_color)

def update_junction_4way(mats, state_str, seq):
    if not state_str: return
    chars_per_approach = len(state_str) // len(seq)
    for i, approach in enumerate(seq):
        m = mats[approach]
        sub_state = state_str[i * chars_per_approach : (i + 1) * chars_per_approach]
        
        set_mat(m['L'], [0.0, 1.0, 0.0]) # Free left always green
        
        if 'G' in sub_state or 'g' in sub_state:
            set_mat(m['R'], [0.0, 0.0, 0.0])
            set_mat(m['Y'], [0.0, 0.0, 0.0])
            set_mat(m['T'], [0.0, 1.0, 0.0])
        elif 'y' in sub_state or 'Y' in sub_state:
            set_mat(m['R'], [0.0, 0.0, 0.0])
            set_mat(m['Y'], [1.0, 0.65, 0.0])
            set_mat(m['T'], [0.0, 0.0, 0.0])
        else:
            set_mat(m['R'], [1.0, 0.0, 0.0])
            set_mat(m['Y'], [0.0, 0.0, 0.0])
            set_mat(m['T'], [0.0, 0.0, 0.0])

def parse_latest_states(filepath):
    states = {"25": None, "26": None, "27": None}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in reversed(lines):
            if '<tlsState ' in line:
                m_id = re.search(r'id="([^"]+)"', line)
                m_state = re.search(r'state="([^"]+)"', line)
                if m_id and m_state:
                    tid = m_id.group(1)
                    if tid in states and states[tid] is None:
                        states[tid] = m_state.group(1)
            if all(v is not None for v in states.values()):
                break
    except Exception:
        pass
    return states

def update_j41(mats, state_str):
    if not state_str or len(state_str) < 8: return
    # Indices 0,1,2 and 5,6,7 belong to MAIN
    # Indices 3,4 belong to SHORTCUT
    main_green = any(c in 'Gg' for i, c in enumerate(state_str) if i in (0,1,2,5,6,7))
    main_amber = any(c in 'yY' for i, c in enumerate(state_str) if i in (0,1,2,5,6,7))
    
    short_green = any(c in 'Gg' for i, c in enumerate(state_str) if i in (3,4))
    short_amber = any(c in 'yY' for i, c in enumerate(state_str) if i in (3,4))

    set_mat(mats['MAIN']['T'], GREEN_ON if main_green else OFF)
    set_mat(mats['MAIN']['L'], GREEN_ON)
    set_mat(mats['MAIN']['R'], RED_ON if not main_green and not main_amber else OFF)
    set_mat(mats['MAIN']['Y'], AMBER_ON if main_amber and not main_green else OFF)

    set_mat(mats['SHORTCUT']['T'], GREEN_ON if short_green else OFF)
    set_mat(mats['SHORTCUT']['L'], GREEN_ON)
    set_mat(mats['SHORTCUT']['R'], RED_ON if not short_green and not short_amber else OFF)
    set_mat(mats['SHORTCUT']['Y'], AMBER_ON if short_amber and not short_green else OFF)

def update_j43(mats, state_str):
    if not state_str or len(state_str) < 8: return
    # Indices 0,1,2,3,4,5 belong to MAIN (EAST/WEST faces)
    # Indices 6,7 belong to SHORTCUT
    main_green = any(c in 'Gg' for i, c in enumerate(state_str) if i in (0,1,2,3,4,5))
    main_amber = any(c in 'yY' for i, c in enumerate(state_str) if i in (0,1,2,3,4,5))
    
    short_green = any(c in 'Gg' for i, c in enumerate(state_str) if i in (6,7))
    short_amber = any(c in 'yY' for i, c in enumerate(state_str) if i in (6,7))

    for approach in ['EAST', 'WEST']:
        set_mat(mats[approach]['T'], GREEN_ON if main_green else OFF)
        set_mat(mats[approach]['L'], GREEN_ON)
        set_mat(mats[approach]['R'], RED_ON if not main_green and not main_amber else OFF)
        set_mat(mats[approach]['Y'], AMBER_ON if main_amber and not main_green else OFF)

    set_mat(mats['SHORTCUT']['T'], GREEN_ON if short_green else OFF)
    set_mat(mats['SHORTCUT']['L'], GREEN_ON)
    set_mat(mats['SHORTCUT']['R'], RED_ON if not short_green and not short_amber else OFF)
    set_mat(mats['SHORTCUT']['Y'], AMBER_ON if short_amber and not short_green else OFF)

def main():
    robot = Supervisor()
    timestep = int(robot.getBasicTimeStep())
    if timestep <= 0: timestep = 32

    RED_ON   = [1.0, 0.0, 0.0]
    AMBER_ON = [1.0, 0.65, 0.0]
    GREEN_ON = [0.0, 1.0, 0.0]
    OFF      = [0.0, 0.0, 0.0]

    # Initialize Mats
    mats_25 = {
        'EAST':  {'R': robot.getFromDef("MAT_25_EAST_RED"),  'Y': robot.getFromDef("MAT_25_EAST_AMBER"),  'L': robot.getFromDef("MAT_25_EAST_LEFT"),  'T': robot.getFromDef("MAT_25_EAST_RIGHT")},
        'NORTH': {'R': robot.getFromDef("MAT_25_NORTH_RED"), 'Y': robot.getFromDef("MAT_25_NORTH_AMBER"), 'L': robot.getFromDef("MAT_25_NORTH_LEFT"), 'T': robot.getFromDef("MAT_25_NORTH_RIGHT")},
        'WEST':  {'R': robot.getFromDef("MAT_25_WEST_RED"),  'Y': robot.getFromDef("MAT_25_WEST_AMBER"),  'L': robot.getFromDef("MAT_25_WEST_LEFT"),  'T': robot.getFromDef("MAT_25_WEST_RIGHT")},
        'SOUTH': {'R': robot.getFromDef("MAT_25_SOUTH_RED"), 'Y': robot.getFromDef("MAT_25_SOUTH_AMBER"), 'L': robot.getFromDef("MAT_25_SOUTH_LEFT"), 'T': robot.getFromDef("MAT_25_SOUTH_RIGHT")},
    }
    mats_26 = {
        'SOUTH': {'R': robot.getFromDef("MAT_26_SOUTH_RED"), 'Y': robot.getFromDef("MAT_26_SOUTH_AMBER"), 'L': robot.getFromDef("MAT_26_SOUTH_LEFT"), 'T': robot.getFromDef("MAT_26_SOUTH_RIGHT")},
        'EAST':  {'R': robot.getFromDef("MAT_26_EAST_RED"),  'Y': robot.getFromDef("MAT_26_EAST_AMBER"),  'L': robot.getFromDef("MAT_26_EAST_LEFT"),  'T': robot.getFromDef("MAT_26_EAST_RIGHT")},
        'NORTH': {'R': robot.getFromDef("MAT_26_NORTH_RED"), 'Y': robot.getFromDef("MAT_26_NORTH_AMBER"), 'L': robot.getFromDef("MAT_26_NORTH_LEFT"), 'T': robot.getFromDef("MAT_26_NORTH_RIGHT")},
        'WEST':  {'R': robot.getFromDef("MAT_26_WEST_RED"),  'Y': robot.getFromDef("MAT_26_WEST_AMBER"),  'L': robot.getFromDef("MAT_26_WEST_LEFT"),  'T': robot.getFromDef("MAT_26_WEST_RIGHT")},
    }
    mats_27 = {
        'SOUTH': {'R': robot.getFromDef("MAT_27_SOUTH_RED"), 'Y': robot.getFromDef("MAT_27_SOUTH_AMBER"), 'L': robot.getFromDef("MAT_27_SOUTH_LEFT"), 'T': robot.getFromDef("MAT_27_SOUTH_RIGHT")},
        'EAST':  {'R': robot.getFromDef("MAT_27_EAST_RED"),  'Y': robot.getFromDef("MAT_27_EAST_AMBER"),  'L': robot.getFromDef("MAT_27_EAST_LEFT"),  'T': robot.getFromDef("MAT_27_EAST_RIGHT")},
        'NORTH': {'R': robot.getFromDef("MAT_27_NORTH_RED"), 'Y': robot.getFromDef("MAT_27_NORTH_AMBER"), 'L': robot.getFromDef("MAT_27_NORTH_LEFT"), 'T': robot.getFromDef("MAT_27_NORTH_RIGHT")},
        'WEST':  {'R': robot.getFromDef("MAT_27_WEST_RED"),  'Y': robot.getFromDef("MAT_27_WEST_AMBER"),  'L': robot.getFromDef("MAT_27_WEST_LEFT"),  'T': robot.getFromDef("MAT_27_WEST_RIGHT")},
    }
    mats_41 = {
        'MAIN':     {'R': robot.getFromDef("MAT_41_MAIN_RED"),     'Y': robot.getFromDef("MAT_41_MAIN_AMBER"),     'L': robot.getFromDef("MAT_41_MAIN_LEFT"),     'T': robot.getFromDef("MAT_41_MAIN_RIGHT")},
        'SHORTCUT': {'R': robot.getFromDef("MAT_41_SHORTCUT_RED"), 'Y': robot.getFromDef("MAT_41_SHORTCUT_AMBER"), 'L': robot.getFromDef("MAT_41_SHORTCUT_LEFT"), 'T': robot.getFromDef("MAT_41_SHORTCUT_RIGHT")},
    }
    mats_43 = {
        'EAST':     {'R': robot.getFromDef("MAT_43_EAST_RED"),     'Y': robot.getFromDef("MAT_43_EAST_AMBER"),     'L': robot.getFromDef("MAT_43_EAST_LEFT"),     'T': robot.getFromDef("MAT_43_EAST_RIGHT")},
        'WEST':     {'R': robot.getFromDef("MAT_43_WEST_RED"),     'Y': robot.getFromDef("MAT_43_WEST_AMBER"),     'L': robot.getFromDef("MAT_43_WEST_LEFT"),     'T': robot.getFromDef("MAT_43_WEST_RIGHT")},
        'SHORTCUT': {'R': robot.getFromDef("MAT_43_SHORTCUT_RED"), 'Y': robot.getFromDef("MAT_43_SHORTCUT_AMBER"), 'L': robot.getFromDef("MAT_43_SHORTCUT_LEFT"), 'T': robot.getFromDef("MAT_43_SHORTCUT_RIGHT")},
    }

    print("Traffic Light Supervisor Operating in Asynchronous XML Parsing Mode.", flush=True)

    # SUMO typically runs from worlds/
    xml_path = os.path.join(os.path.dirname(__file__), "..", "..", "worlds", "sih_mvp_traffic_net", "tls_switch.xml")

    # Wipe old file if it exists to prevent reading previous run data
    if os.path.exists(xml_path):
        try:
            os.remove(xml_path)
        except Exception:
            pass

    # Default static phases so it doesn't stay black before SUMO switches lights
    last_states = {
        "25": "GGGggrrrrrrrrrrrrrrr",
        "26": "GGGggrrrrrrrrrrrrrrr",
        "27": "GGGggrrrrrrrrrrrrrrr",
        "41": "GGgrrGGg",
        "43": "gGGGGgrr"
    }

    while robot.step(timestep) != -1:
        sim_time = robot.getTime()

        # Parse intelligent states from SUMO asynchronously
        new_states = parse_latest_states(xml_path)
        for k in last_states.keys():
            if new_states.get(k):
                last_states[k] = new_states[k]

        update_junction_4way(mats_25, last_states["25"], ['EAST', 'NORTH', 'WEST', 'SOUTH'])
        update_junction_4way(mats_26, last_states["26"], ['SOUTH', 'EAST', 'NORTH', 'WEST'])
        update_junction_4way(mats_27, last_states["27"], ['SOUTH', 'EAST', 'NORTH', 'WEST'])
        
        update_j41(mats_41, last_states.get("41", ""))
        update_j43(mats_43, last_states.get("43", ""))

if __name__ == '__main__':
    main()
