"""
traffic_light_controller.py — Rapid 28s Indian Traffic Light Supervisor in Webots.

Deterministic Clean Signal Logic:
1. GREEN Phase:
   - RED is strictly OFF.
   - AMBER is strictly OFF.
   - STRAIGHT GREEN is ON.
   - TURN ARROWS (Left or Right) are ON if active for that phase.
2. AMBER Phase:
   - RED is strictly OFF.
   - AMBER is ON.
   - STRAIGHT and ARROWS are strictly OFF.
3. RED Phase:
   - RED is ON.
   - AMBER is strictly OFF.
   - STRAIGHT and RIGHT ARROWS are strictly OFF.
   - FREE-LEFT ARROW is ON ONLY if free_left=True (Free Left on Red).

Synchronized with SUMO across all junctions:
- Junctions 25, 26, 27: 4-Way 28s Cycle (4 stages * 7s).
- Junction 41 (Left End of Shortcut Parkway at -45.0, 4.5):
  * Phase 0 (0-12s): North-South Main Road GREEN (South Straight + Right ON; North Straight + Left ON; East Red + Free-Left ON).
  * Amber (12-14s): South & North AMBER; East Red + Free-Left.
  * Phase 1 (14-26s): East Merging Shortcut GREEN (East Right ON + Free-Left ON; South & North RED).
  * Amber (26-28s): East AMBER; South & North RED.
- Junction 43 (Right End of Shortcut Parkway at +45.0, 4.5):
  * Phase 0 (0-12s): North-South Main Road GREEN (South Straight + Left ON; North Straight + Right ON; West Red + Free-Left ON).
  * Amber (12-14s): South & North AMBER; West Red + Free-Left.
  * Phase 1 (14-26s): West Merging Shortcut GREEN (West Right ON + Free-Left ON; South & North RED).
  * Amber (26-28s): West AMBER; South & North RED.
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
    elif '43' in robot_name:
        j_id = '43'
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
    RED_OFF  = [0.05, 0.01, 0.01]

    AMBER_ON  = [1.0, 0.65, 0.05]
    AMBER_OFF = [0.05, 0.03, 0.0]

    GREEN_ON  = [0.1, 1.0, 0.3]
    GREEN_OFF = [0.0, 0.05, 0.01]

    def set_approach_state(dir_name, state, left_arrow=False, right_arrow=False, free_left_on_red=False):
        fields = emissive_fields.get(dir_name, {})
        if not fields:
            return
        
        if state == 'GREEN':
            # Pure Green: Red OFF, Amber OFF, Straight ON, Arrows as specified
            if 'RED' in fields: fields['RED'].setSFColor(RED_OFF)
            if 'AMBER' in fields: fields['AMBER'].setSFColor(AMBER_OFF)
            if 'STRAIGHT' in fields: fields['STRAIGHT'].setSFColor(GREEN_ON)
            if 'LEFT' in fields: fields['LEFT'].setSFColor(GREEN_ON if left_arrow else GREEN_OFF)
            if 'RIGHT' in fields: fields['RIGHT'].setSFColor(GREEN_ON if right_arrow else GREEN_OFF)

        elif state == 'YELLOW':
            # Pure Yellow: Red OFF, Amber ON, Straight OFF, Arrows OFF
            if 'RED' in fields: fields['RED'].setSFColor(RED_OFF)
            if 'AMBER' in fields: fields['AMBER'].setSFColor(AMBER_ON)
            if 'STRAIGHT' in fields: fields['STRAIGHT'].setSFColor(GREEN_OFF)
            if 'LEFT' in fields: fields['LEFT'].setSFColor(GREEN_OFF)
            if 'RIGHT' in fields: fields['RIGHT'].setSFColor(GREEN_OFF)

        elif state == 'RED':
            # Pure Red: Red ON, Amber OFF, Straight OFF, Right Arrow OFF, Left Arrow ONLY if free_left_on_red is True
            if 'RED' in fields: fields['RED'].setSFColor(RED_ON)
            if 'AMBER' in fields: fields['AMBER'].setSFColor(AMBER_OFF)
            if 'STRAIGHT' in fields: fields['STRAIGHT'].setSFColor(GREEN_OFF)
            if 'LEFT' in fields: fields['LEFT'].setSFColor(GREEN_ON if free_left_on_red else GREEN_OFF)
            if 'RIGHT' in fields: fields['RIGHT'].setSFColor(GREEN_OFF)

    TOTAL_CYCLE = 28.0

    while robot.step(timestep) != -1:
        sim_time = robot.getTime()
        cycle_t = sim_time % TOTAL_CYCLE

        if j_id == '41':
            # Left end of shortcut:
            # - 0-12s: North-South Main Road GREEN
            #   * South: Straight GREEN + Right turn ON into shortcut
            #   * North: Straight GREEN + Left turn ON into shortcut
            #   * East (Shortcut): RED + Free-Left ON (merging South)
            # - 12-14s: North-South AMBER
            # - 14-26s: East Merging Shortcut GREEN (Right turn ON to North + Free-Left ON to South; North-South RED)
            # - 26-28s: East AMBER
            if cycle_t < 12.0:
                set_approach_state('SOUTH', 'GREEN', left_arrow=False, right_arrow=True)
                set_approach_state('NORTH', 'GREEN', left_arrow=True,  right_arrow=False)
                set_approach_state('EAST',  'RED',   free_left_on_red=True)
            elif cycle_t < 14.0:
                set_approach_state('SOUTH', 'YELLOW')
                set_approach_state('NORTH', 'YELLOW')
                set_approach_state('EAST',  'RED',   free_left_on_red=True)
            elif cycle_t < 26.0:
                set_approach_state('SOUTH', 'RED',   free_left_on_red=False)
                set_approach_state('NORTH', 'RED',   free_left_on_red=False)
                set_approach_state('EAST',  'GREEN', left_arrow=True,  right_arrow=True)
            else:
                set_approach_state('SOUTH', 'RED',   free_left_on_red=False)
                set_approach_state('NORTH', 'RED',   free_left_on_red=False)
                set_approach_state('EAST',  'YELLOW')

        elif j_id == '43':
            # Right end of shortcut:
            # - 0-12s: North-South Main Road GREEN
            #   * South: Straight GREEN + Left turn ON into shortcut
            #   * North: Straight GREEN + Right turn ON into shortcut
            #   * West (Shortcut): RED + Free-Left ON (merging North)
            # - 12-14s: North-South AMBER
            # - 14-26s: West Merging Shortcut GREEN (Right turn ON to South + Free-Left ON to North; North-South RED)
            # - 26-28s: West AMBER
            if cycle_t < 12.0:
                set_approach_state('SOUTH', 'GREEN', left_arrow=True,  right_arrow=False)
                set_approach_state('NORTH', 'GREEN', left_arrow=False, right_arrow=True)
                set_approach_state('WEST',  'RED',   free_left_on_red=True)
            elif cycle_t < 14.0:
                set_approach_state('SOUTH', 'YELLOW')
                set_approach_state('NORTH', 'YELLOW')
                set_approach_state('WEST',  'RED',   free_left_on_red=True)
            elif cycle_t < 26.0:
                set_approach_state('SOUTH', 'RED',   free_left_on_red=False)
                set_approach_state('NORTH', 'RED',   free_left_on_red=False)
                set_approach_state('WEST',  'GREEN', left_arrow=True,  right_arrow=True)
            else:
                set_approach_state('SOUTH', 'RED',   free_left_on_red=False)
                set_approach_state('NORTH', 'RED',   free_left_on_red=False)
                set_approach_state('WEST',  'YELLOW')

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
                        set_approach_state(d, 'YELLOW')
                else:
                    # 24/7 Free Left on Red enabled for standard 4-way intersections
                    set_approach_state(d, 'RED', free_left_on_red=True)

if __name__ == '__main__':
    main()
