"""
traffic_light_controller.py — Synchronized Indian Free Left Traffic Signal Controller.

Indian Left-Hand Drive Traffic Rules:
1. Free Left Turn:
   - Green Left Arrow is PERPETUALLY ILLUMINATED (100% Free Left).
   - Left-turning vehicles in Lane 0 proceed continuously.
2. Through & Right Turns:
   - Synchronized 28.0s 4-Stage Cycle (5.0s Green + 2.0s Amber per approach).
"""

from controller import Supervisor

def set_mat(mat_node, on_color):
    if mat_node:
        mat_node.getField("emissiveColor").setSFColor(on_color)

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

    print("Traffic Light Supervisor Online with Indian Free Left Turns Active.")

    TOTAL_CYCLE = 28.0
    STAGE_LEN = 7.0
    GREEN_TIME = 5.0

    while robot.step(timestep) != -1:
        sim_time = robot.getTime()
        cycle_t = sim_time % TOTAL_CYCLE
        stage_idx = int(cycle_t // STAGE_LEN)
        t_in_stage = cycle_t % STAGE_LEN

        # 1. 4-Way 4-Stage Control for J25, J26, J27
        for j_mats, seq in [(mats_25, ['EAST', 'NORTH', 'WEST', 'SOUTH']),
                            (mats_26, ['SOUTH', 'EAST', 'NORTH', 'WEST']),
                            (mats_27, ['SOUTH', 'EAST', 'NORTH', 'WEST'])]:
            for idx, approach in enumerate(seq):
                m = j_mats[approach]
                # FREE LEFT: Green Left Arrow is ALWAYS ON
                set_mat(m['L'], GREEN_ON)

                if idx == stage_idx:
                    if t_in_stage < GREEN_TIME:
                        # Green Phase
                        set_mat(m['R'], OFF)
                        set_mat(m['Y'], OFF)
                        set_mat(m['T'], GREEN_ON)
                    else:
                        # Amber Phase
                        set_mat(m['R'], OFF)
                        set_mat(m['Y'], AMBER_ON)
                        set_mat(m['T'], OFF)
                else:
                    # Red Phase for Through/Right
                    set_mat(m['R'], RED_ON)
                    set_mat(m['Y'], OFF)
                    set_mat(m['T'], OFF)

        # 2. 3-Way Control for J41 & J43
        if cycle_t < 12.0:
            # Main Green, Shortcut Red (Shortcut Free Left Active)
            set_mat(mats_41['MAIN']['R'], OFF); set_mat(mats_41['MAIN']['Y'], OFF); set_mat(mats_41['MAIN']['T'], GREEN_ON); set_mat(mats_41['MAIN']['L'], GREEN_ON)
            set_mat(mats_41['SHORTCUT']['R'], RED_ON); set_mat(mats_41['SHORTCUT']['Y'], OFF); set_mat(mats_41['SHORTCUT']['T'], OFF); set_mat(mats_41['SHORTCUT']['L'], GREEN_ON)
            set_mat(mats_43['EAST']['R'], OFF); set_mat(mats_43['EAST']['Y'], OFF); set_mat(mats_43['EAST']['T'], GREEN_ON); set_mat(mats_43['EAST']['L'], GREEN_ON)
            set_mat(mats_43['WEST']['R'], OFF); set_mat(mats_43['WEST']['Y'], OFF); set_mat(mats_43['WEST']['T'], GREEN_ON); set_mat(mats_43['WEST']['L'], GREEN_ON)
            set_mat(mats_43['SHORTCUT']['R'], RED_ON); set_mat(mats_43['SHORTCUT']['Y'], OFF); set_mat(mats_43['SHORTCUT']['T'], OFF); set_mat(mats_43['SHORTCUT']['L'], GREEN_ON)
        elif cycle_t < 14.0:
            # Main Amber
            set_mat(mats_41['MAIN']['R'], OFF); set_mat(mats_41['MAIN']['Y'], AMBER_ON); set_mat(mats_41['MAIN']['T'], OFF); set_mat(mats_41['MAIN']['L'], GREEN_ON)
            set_mat(mats_41['SHORTCUT']['R'], RED_ON); set_mat(mats_41['SHORTCUT']['Y'], OFF); set_mat(mats_41['SHORTCUT']['T'], OFF); set_mat(mats_41['SHORTCUT']['L'], GREEN_ON)
            set_mat(mats_43['EAST']['R'], OFF); set_mat(mats_43['EAST']['Y'], AMBER_ON); set_mat(mats_43['EAST']['T'], OFF); set_mat(mats_43['EAST']['L'], GREEN_ON)
            set_mat(mats_43['WEST']['R'], OFF); set_mat(mats_43['WEST']['Y'], AMBER_ON); set_mat(mats_43['WEST']['T'], OFF); set_mat(mats_43['WEST']['L'], GREEN_ON)
            set_mat(mats_43['SHORTCUT']['R'], RED_ON); set_mat(mats_43['SHORTCUT']['Y'], OFF); set_mat(mats_43['SHORTCUT']['T'], OFF); set_mat(mats_43['SHORTCUT']['L'], GREEN_ON)
        elif cycle_t < 26.0:
            # Shortcut Green, Main Red
            set_mat(mats_41['MAIN']['R'], RED_ON); set_mat(mats_41['MAIN']['Y'], OFF); set_mat(mats_41['MAIN']['T'], OFF); set_mat(mats_41['MAIN']['L'], GREEN_ON)
            set_mat(mats_41['SHORTCUT']['R'], OFF); set_mat(mats_41['SHORTCUT']['Y'], OFF); set_mat(mats_41['SHORTCUT']['T'], GREEN_ON); set_mat(mats_41['SHORTCUT']['L'], GREEN_ON)
            set_mat(mats_43['EAST']['R'], RED_ON); set_mat(mats_43['EAST']['Y'], OFF); set_mat(mats_43['EAST']['T'], OFF); set_mat(mats_43['EAST']['L'], GREEN_ON)
            set_mat(mats_43['WEST']['R'], RED_ON); set_mat(mats_43['WEST']['Y'], OFF); set_mat(mats_43['WEST']['T'], OFF); set_mat(mats_43['WEST']['L'], GREEN_ON)
            set_mat(mats_43['SHORTCUT']['R'], OFF); set_mat(mats_43['SHORTCUT']['Y'], OFF); set_mat(mats_43['SHORTCUT']['T'], GREEN_ON); set_mat(mats_43['SHORTCUT']['L'], GREEN_ON)
        else:
            # Shortcut Amber
            set_mat(mats_41['MAIN']['R'], RED_ON); set_mat(mats_41['MAIN']['Y'], OFF); set_mat(mats_41['MAIN']['T'], OFF); set_mat(mats_41['MAIN']['L'], GREEN_ON)
            set_mat(mats_41['SHORTCUT']['R'], OFF); set_mat(mats_41['SHORTCUT']['Y'], AMBER_ON); set_mat(mats_41['SHORTCUT']['T'], OFF); set_mat(mats_41['SHORTCUT']['L'], GREEN_ON)
            set_mat(mats_43['EAST']['R'], RED_ON); set_mat(mats_43['EAST']['Y'], OFF); set_mat(mats_43['EAST']['T'], OFF); set_mat(mats_43['EAST']['L'], GREEN_ON)
            set_mat(mats_43['WEST']['R'], RED_ON); set_mat(mats_43['WEST']['Y'], OFF); set_mat(mats_43['WEST']['T'], OFF); set_mat(mats_43['WEST']['L'], GREEN_ON)
            set_mat(mats_43['SHORTCUT']['R'], OFF); set_mat(mats_43['SHORTCUT']['Y'], AMBER_ON); set_mat(mats_43['SHORTCUT']['T'], OFF); set_mat(mats_43['SHORTCUT']['L'], GREEN_ON)

if __name__ == '__main__':
    main()
