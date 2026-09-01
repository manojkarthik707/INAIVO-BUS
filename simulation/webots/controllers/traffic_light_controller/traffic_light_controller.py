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
        "27": "GGGggrrrrrrrrrrrrrrr"
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

        # Static 3-Way Control for J41 & J43
        cycle_t = sim_time % 28.0
        if cycle_t < 12.0:
            set_mat(mats_41['MAIN']['R'], OFF); set_mat(mats_41['MAIN']['Y'], OFF); set_mat(mats_41['MAIN']['T'], GREEN_ON); set_mat(mats_41['MAIN']['L'], GREEN_ON)
            set_mat(mats_41['SHORTCUT']['R'], RED_ON); set_mat(mats_41['SHORTCUT']['Y'], OFF); set_mat(mats_41['SHORTCUT']['T'], OFF); set_mat(mats_41['SHORTCUT']['L'], GREEN_ON)
            set_mat(mats_43['EAST']['R'], OFF); set_mat(mats_43['EAST']['Y'], OFF); set_mat(mats_43['EAST']['T'], GREEN_ON); set_mat(mats_43['EAST']['L'], GREEN_ON)
            set_mat(mats_43['WEST']['R'], OFF); set_mat(mats_43['WEST']['Y'], OFF); set_mat(mats_43['WEST']['T'], GREEN_ON); set_mat(mats_43['WEST']['L'], GREEN_ON)
            set_mat(mats_43['SHORTCUT']['R'], RED_ON); set_mat(mats_43['SHORTCUT']['Y'], OFF); set_mat(mats_43['SHORTCUT']['T'], OFF); set_mat(mats_43['SHORTCUT']['L'], GREEN_ON)
        elif cycle_t < 14.0:
            set_mat(mats_41['MAIN']['R'], OFF); set_mat(mats_41['MAIN']['Y'], AMBER_ON); set_mat(mats_41['MAIN']['T'], OFF); set_mat(mats_41['MAIN']['L'], GREEN_ON)
            set_mat(mats_41['SHORTCUT']['R'], RED_ON); set_mat(mats_41['SHORTCUT']['Y'], OFF); set_mat(mats_41['SHORTCUT']['T'], OFF); set_mat(mats_41['SHORTCUT']['L'], GREEN_ON)
            set_mat(mats_43['EAST']['R'], OFF); set_mat(mats_43['EAST']['Y'], AMBER_ON); set_mat(mats_43['EAST']['T'], OFF); set_mat(mats_43['EAST']['L'], GREEN_ON)
            set_mat(mats_43['WEST']['R'], OFF); set_mat(mats_43['WEST']['Y'], AMBER_ON); set_mat(mats_43['WEST']['T'], OFF); set_mat(mats_43['WEST']['L'], GREEN_ON)
            set_mat(mats_43['SHORTCUT']['R'], RED_ON); set_mat(mats_43['SHORTCUT']['Y'], OFF); set_mat(mats_43['SHORTCUT']['T'], OFF); set_mat(mats_43['SHORTCUT']['L'], GREEN_ON)
        elif cycle_t < 26.0:
            set_mat(mats_41['MAIN']['R'], RED_ON); set_mat(mats_41['MAIN']['Y'], OFF); set_mat(mats_41['MAIN']['T'], OFF); set_mat(mats_41['MAIN']['L'], GREEN_ON)
            set_mat(mats_41['SHORTCUT']['R'], OFF); set_mat(mats_41['SHORTCUT']['Y'], OFF); set_mat(mats_41['SHORTCUT']['T'], GREEN_ON); set_mat(mats_41['SHORTCUT']['L'], GREEN_ON)
            set_mat(mats_43['EAST']['R'], RED_ON); set_mat(mats_43['EAST']['Y'], OFF); set_mat(mats_43['EAST']['T'], OFF); set_mat(mats_43['EAST']['L'], GREEN_ON)
            set_mat(mats_43['WEST']['R'], RED_ON); set_mat(mats_43['WEST']['Y'], OFF); set_mat(mats_43['WEST']['T'], OFF); set_mat(mats_43['WEST']['L'], GREEN_ON)
            set_mat(mats_43['SHORTCUT']['R'], OFF); set_mat(mats_43['SHORTCUT']['Y'], OFF); set_mat(mats_43['SHORTCUT']['T'], GREEN_ON); set_mat(mats_43['SHORTCUT']['L'], GREEN_ON)
        else:
            set_mat(mats_41['MAIN']['R'], RED_ON); set_mat(mats_41['MAIN']['Y'], OFF); set_mat(mats_41['MAIN']['T'], OFF); set_mat(mats_41['MAIN']['L'], GREEN_ON)
            set_mat(mats_41['SHORTCUT']['R'], OFF); set_mat(mats_41['SHORTCUT']['Y'], AMBER_ON); set_mat(mats_41['SHORTCUT']['T'], OFF); set_mat(mats_41['SHORTCUT']['L'], GREEN_ON)
            set_mat(mats_43['EAST']['R'], RED_ON); set_mat(mats_43['EAST']['Y'], OFF); set_mat(mats_43['EAST']['T'], OFF); set_mat(mats_43['EAST']['L'], GREEN_ON)
            set_mat(mats_43['WEST']['R'], RED_ON); set_mat(mats_43['WEST']['Y'], OFF); set_mat(mats_43['WEST']['T'], OFF); set_mat(mats_43['WEST']['L'], GREEN_ON)
            set_mat(mats_43['SHORTCUT']['R'], OFF); set_mat(mats_43['SHORTCUT']['Y'], AMBER_ON); set_mat(mats_43['SHORTCUT']['T'], OFF); set_mat(mats_43['SHORTCUT']['L'], GREEN_ON)

if __name__ == '__main__':
    main()
