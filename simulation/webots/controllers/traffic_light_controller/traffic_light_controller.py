"""
traffic_light_controller.py — Rapid 28s Indian Traffic Light Supervisor in Webots.

Synchronized with SUMO static cycle:
- Junctions 25, 26, 27: 4-Way 28s Cycle (4 stages * 7s).
- Junction 41 (Merging 3-Way T-Junction at Shortcut Road):
  * Phase 0 (0-12s): North-South Main Road GREEN (South Straight + Right turn ON into shortcut; North Straight + Left turn ON into shortcut; East Shortcut shows Red + Free-Left ON).
  * Amber (12-14s): South & North AMBER; East shows Red + Free-Left.
  * Phase 1 (14-26s): East Merging Shortcut Road GREEN (East Straight + Right turn ON + Free-Left ON; South & North Main Road shows Red).
  * Amber (26-28s): East AMBER; South & North Main Road shows Red.
"""

from controller import Supervisor

def main():
    robot = Supervisor()
    timestep = int(robot.getBasicTimeStep())
    if timestep <= 0:
        timestep = 32

    robot_name = robot.getName().lower()
    
    if '25' in robot_name:
        j_id = '25'
    elif '26' in robot_name:
        j_id = '26'
    elif '27' in robot_name:
        j_id = '27'
    elif '41' in robot_name:
        j_id = '41'
    else:
        j_id = '25'

    directions = ['NORTH', 'SOUTH', 'EAST', 'WEST']
    aspects = ['RED', 'AMBER', 'STRAIGHT', 'LEFT', 'RIGHT']

    # Discover and cache emissiveColor shader fields
    emissive_fields = {}
    for d in directions:
        emissive_fields[d] = {}
        for a in aspects:
            def_name = f"MAT_{j_id}_{d}_{a}"
            node = robot.getFromDef(def_name)
            if node:
                field = node.getField("emissiveColor")
                if field:
                    emissive_fields[d][a] = field

    print(f"TrafficLight Supervisor for Junction {j_id} online: {sum(len(d) for d in emissive_fields.values())} shaders bound.")

    # High-intensity active LED colors vs dark off colors
    RED_ON   = [1.0, 0.05, 0.05]
    RED_OFF  = [0.08, 0.01, 0.01]

    AMBER_ON  = [1.0, 0.65, 0.05]
    AMBER_OFF = [0.06, 0.03, 0.0]

    GREEN_ON  = [0.1, 1.0, 0.3]
    GREEN_OFF = [0.0, 0.05, 0.01]

    def set_approach_state(dir_name, state, left_arrow=False, right_arrow=False):
        fields = emissive_fields.get(dir_name, {})
        if not fields:
            return
        
        if state == 'GREEN':
            if 'RED' in fields: fields['RED'].setSFColor(RED_OFF)
            if 'AMBER' in fields: fields['AMBER'].setSFColor(AMBER_OFF)
            if 'STRAIGHT' in fields: fields['STRAIGHT'].setSFColor(GREEN_ON)
            if 'LEFT' in fields: fields['LEFT'].setSFColor(GREEN_ON if left_arrow else GREEN_OFF)
            if 'RIGHT' in fields: fields['RIGHT'].setSFColor(GREEN_ON if right_arrow else GREEN_OFF)

        elif state == 'YELLOW':
            if 'RED' in fields: fields['RED'].setSFColor(RED_OFF)
            if 'AMBER' in fields: fields['AMBER'].setSFColor(AMBER_ON)
            if 'STRAIGHT' in fields: fields['STRAIGHT'].setSFColor(GREEN_OFF)
            if 'LEFT' in fields: fields['LEFT'].setSFColor(GREEN_ON if left_arrow else GREEN_OFF)
            if 'RIGHT' in fields: fields['RIGHT'].setSFColor(GREEN_OFF)

        elif state == 'RED':
            if 'RED' in fields: fields['RED'].setSFColor(RED_ON)
            if 'AMBER' in fields: fields['AMBER'].setSFColor(AMBER_OFF)
            if 'STRAIGHT' in fields: fields['STRAIGHT'].setSFColor(GREEN_OFF)
            if 'LEFT' in fields: fields['LEFT'].setSFColor(GREEN_ON if left_arrow else GREEN_OFF)
            if 'RIGHT' in fields: fields['RIGHT'].setSFColor(GREEN_OFF)

    TOTAL_CYCLE = 28.0

    while robot.step(timestep) != -1:
        sim_time = robot.getTime()
        cycle_t = sim_time % TOTAL_CYCLE

        if j_id == '41':
            # 3-Way T-Junction:
            # - 0-12s: North-South Main Road GREEN
            #   * South: Straight GREEN + RIGHT turn arrow ON (turns East into shortcut)
            #   * North: Straight GREEN + LEFT turn arrow ON (turns East into shortcut)
            #   * East: RED + Free-Left ON
            # - 12-14s: North-South AMBER
            # - 14-26s: East Merging Shortcut Road GREEN
            #   * East: Straight GREEN + RIGHT turn arrow ON + Free-Left ON
            #   * South & North: RED
            # - 26-28s: East AMBER
            if cycle_t < 12.0:
                set_approach_state('SOUTH', 'GREEN', left_arrow=False, right_arrow=True)
                set_approach_state('NORTH', 'GREEN', left_arrow=True,  right_arrow=False)
                set_approach_state('EAST',  'RED',   left_arrow=True,  right_arrow=False)
            elif cycle_t < 14.0:
                set_approach_state('SOUTH', 'YELLOW', left_arrow=False, right_arrow=False)
                set_approach_state('NORTH', 'YELLOW', left_arrow=False, right_arrow=False)
                set_approach_state('EAST',  'RED',    left_arrow=True,  right_arrow=False)
            elif cycle_t < 26.0:
                set_approach_state('SOUTH', 'RED',   left_arrow=False, right_arrow=False)
                set_approach_state('NORTH', 'RED',   left_arrow=False, right_arrow=False)
                set_approach_state('EAST',  'GREEN', left_arrow=True,  right_arrow=True)
            else:
                set_approach_state('SOUTH', 'RED',    left_arrow=False, right_arrow=False)
                set_approach_state('NORTH', 'RED',    left_arrow=False, right_arrow=False)
                set_approach_state('EAST',  'YELLOW', left_arrow=True,  right_arrow=False)
        else:
            # 4-Way Standard Junctions (25, 26, 27)
            if j_id == '25':
                stage_sequence = ['EAST', 'NORTH', 'WEST', 'SOUTH']
            else:
                stage_sequence = ['SOUTH', 'EAST', 'NORTH', 'WEST']

            STAGE_LEN = 7.0
            GREEN_LEN = 5.0
            stage_idx = int(cycle_t // STAGE_LEN)
            t_in_stage = cycle_t % STAGE_LEN

            active_dir = stage_sequence[stage_idx]

            for d in ['NORTH', 'SOUTH', 'EAST', 'WEST']:
                if d == active_dir:
                    if t_in_stage < GREEN_LEN:
                        set_approach_state(d, 'GREEN', left_arrow=True, right_arrow=True)
                    else:
                        set_approach_state(d, 'YELLOW', left_arrow=True, right_arrow=False)
                else:
                    set_approach_state(d, 'RED', left_arrow=True, right_arrow=False)

if __name__ == '__main__':
    main()
