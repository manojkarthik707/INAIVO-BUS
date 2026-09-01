"""
traffic_light_controller.py — Synchronized Indian Free Left Traffic Signal Controller.

Indian Left-Hand Drive Traffic Rules:
1. Free Left Turn:
   - Green Left Arrow is PERPETUALLY ILLUMINATED (100% Free Left).
   - Left-turning vehicles in Lane 0 proceed continuously.
2. Through & Right Turns:
   - Synchronized dynamically with SUMO's TraCI for intelligent actuated traffic lights.
"""

import sys
import time
from controller import Supervisor
import traci

def set_mat(mat_node, on_color):
    if mat_node:
        mat_node.getField("emissiveColor").setSFColor(on_color)

def update_junction_4way(mats, state_str, seq):
    # Map SUMO state string (e.g. GGGggrrrrrrrrrrrrrrr) to Webots materials
    # Usually 20 chars, 5 per approach
    chars_per_approach = len(state_str) // len(seq)
    
    for i, approach in enumerate(seq):
        m = mats[approach]
        sub_state = state_str[i * chars_per_approach : (i + 1) * chars_per_approach]
        
        # FREE LEFT: Green Left Arrow is ALWAYS ON
        set_mat(m['L'], [0.0, 1.0, 0.0])
        
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

def main():
    robot = Supervisor()
    timestep = int(robot.getBasicTimeStep())
    if timestep <= 0:
        timestep = 32

    # Active Colors
    RED_ON   = [1.0, 0.0, 0.0]
    AMBER_ON = [1.0, 0.65, 0.0]
    GREEN_ON = [0.0, 1.0, 0.0]
    OFF      = [0.0, 0.0, 0.0]

    # Junction 25
    mats_25 = {
        'EAST':  {'R': robot.getFromDef("MAT_25_EAST_RED"),  'Y': robot.getFromDef("MAT_25_EAST_AMBER"),  'L': robot.getFromDef("MAT_25_EAST_LEFT"),  'T': robot.getFromDef("MAT_25_EAST_RIGHT")},
        'NORTH': {'R': robot.getFromDef("MAT_25_NORTH_RED"), 'Y': robot.getFromDef("MAT_25_NORTH_AMBER"), 'L': robot.getFromDef("MAT_25_NORTH_LEFT"), 'T': robot.getFromDef("MAT_25_NORTH_RIGHT")},
        'WEST':  {'R': robot.getFromDef("MAT_25_WEST_RED"),  'Y': robot.getFromDef("MAT_25_WEST_AMBER"),  'L': robot.getFromDef("MAT_25_WEST_LEFT"),  'T': robot.getFromDef("MAT_25_WEST_RIGHT")},
        'SOUTH': {'R': robot.getFromDef("MAT_25_SOUTH_RED"), 'Y': robot.getFromDef("MAT_25_SOUTH_AMBER"), 'L': robot.getFromDef("MAT_25_SOUTH_LEFT"), 'T': robot.getFromDef("MAT_25_SOUTH_RIGHT")},
    }

    # Junction 26
    mats_26 = {
        'SOUTH': {'R': robot.getFromDef("MAT_26_SOUTH_RED"), 'Y': robot.getFromDef("MAT_26_SOUTH_AMBER"), 'L': robot.getFromDef("MAT_26_SOUTH_LEFT"), 'T': robot.getFromDef("MAT_26_SOUTH_RIGHT")},
        'EAST':  {'R': robot.getFromDef("MAT_26_EAST_RED"),  'Y': robot.getFromDef("MAT_26_EAST_AMBER"),  'L': robot.getFromDef("MAT_26_EAST_LEFT"),  'T': robot.getFromDef("MAT_26_EAST_RIGHT")},
        'NORTH': {'R': robot.getFromDef("MAT_26_NORTH_RED"), 'Y': robot.getFromDef("MAT_26_NORTH_AMBER"), 'L': robot.getFromDef("MAT_26_NORTH_LEFT"), 'T': robot.getFromDef("MAT_26_NORTH_RIGHT")},
        'WEST':  {'R': robot.getFromDef("MAT_26_WEST_RED"),  'Y': robot.getFromDef("MAT_26_WEST_AMBER"),  'L': robot.getFromDef("MAT_26_WEST_LEFT"),  'T': robot.getFromDef("MAT_26_WEST_RIGHT")},
    }

    # Junction 27
    mats_27 = {
        'SOUTH': {'R': robot.getFromDef("MAT_27_SOUTH_RED"), 'Y': robot.getFromDef("MAT_27_SOUTH_AMBER"), 'L': robot.getFromDef("MAT_27_SOUTH_LEFT"), 'T': robot.getFromDef("MAT_27_SOUTH_RIGHT")},
        'EAST':  {'R': robot.getFromDef("MAT_27_EAST_RED"),  'Y': robot.getFromDef("MAT_27_EAST_AMBER"),  'L': robot.getFromDef("MAT_27_EAST_LEFT"),  'T': robot.getFromDef("MAT_27_EAST_RIGHT")},
        'NORTH': {'R': robot.getFromDef("MAT_27_NORTH_RED"), 'Y': robot.getFromDef("MAT_27_NORTH_AMBER"), 'L': robot.getFromDef("MAT_27_NORTH_LEFT"), 'T': robot.getFromDef("MAT_27_NORTH_RIGHT")},
        'WEST':  {'R': robot.getFromDef("MAT_27_WEST_RED"),  'Y': robot.getFromDef("MAT_27_WEST_AMBER"),  'L': robot.getFromDef("MAT_27_WEST_LEFT"),  'T': robot.getFromDef("MAT_27_WEST_RIGHT")},
    }

    # Junction 41 & 43
    mats_41 = {
        'MAIN':     {'R': robot.getFromDef("MAT_41_MAIN_RED"),     'Y': robot.getFromDef("MAT_41_MAIN_AMBER"),     'L': robot.getFromDef("MAT_41_MAIN_LEFT"),     'T': robot.getFromDef("MAT_41_MAIN_RIGHT")},
        'SHORTCUT': {'R': robot.getFromDef("MAT_41_SHORTCUT_RED"), 'Y': robot.getFromDef("MAT_41_SHORTCUT_AMBER"), 'L': robot.getFromDef("MAT_41_SHORTCUT_LEFT"), 'T': robot.getFromDef("MAT_41_SHORTCUT_RIGHT")},
    }
    mats_43 = {
        'EAST':     {'R': robot.getFromDef("MAT_43_EAST_RED"),     'Y': robot.getFromDef("MAT_43_EAST_AMBER"),     'L': robot.getFromDef("MAT_43_EAST_LEFT"),     'T': robot.getFromDef("MAT_43_EAST_RIGHT")},
        'WEST':     {'R': robot.getFromDef("MAT_43_WEST_RED"),     'Y': robot.getFromDef("MAT_43_WEST_AMBER"),     'L': robot.getFromDef("MAT_43_WEST_LEFT"),     'T': robot.getFromDef("MAT_43_WEST_RIGHT")},
        'SHORTCUT': {'R': robot.getFromDef("MAT_43_SHORTCUT_RED"), 'Y': robot.getFromDef("MAT_43_SHORTCUT_AMBER"), 'L': robot.getFromDef("MAT_43_SHORTCUT_LEFT"), 'T': robot.getFromDef("MAT_43_SHORTCUT_RIGHT")},
    }

    print("Traffic Light Supervisor Connecting to TraCI for Intelligent Sync...")
    
    # Wait for sumo_supervisor to start SUMO
    traci_connected = False
    for _ in range(20):
        try:
            traci.setOrder(2)
            traci.connect(port=8873, numRetries=5)
            traci_connected = True
            print("TraCI Connected Successfully! Intelligent Traffic Lights Synced.")
            break
        except Exception as e:
            time.sleep(1)
            
    if not traci_connected:
        print("WARNING: Could not connect to TraCI. Traffic lights will run in static fallback mode.")

    while robot.step(timestep) != -1:
        sim_time = robot.getTime()

        if traci_connected:
            try:
                state_25 = traci.trafficlight.getRedYellowGreenState("25")
                state_26 = traci.trafficlight.getRedYellowGreenState("26")
                state_27 = traci.trafficlight.getRedYellowGreenState("27")
                
                update_junction_4way(mats_25, state_25, ['EAST', 'NORTH', 'WEST', 'SOUTH'])
                update_junction_4way(mats_26, state_26, ['SOUTH', 'EAST', 'NORTH', 'WEST'])
                update_junction_4way(mats_27, state_27, ['SOUTH', 'EAST', 'NORTH', 'WEST'])
            except Exception as e:
                pass

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
