"""
traffic_light_controller.py — Clean, Deterministic Indian Traffic Light Supervisor.

Strict Mutually-Exclusive State Guarantees:
1. GREEN:
   - RED is strictly OFF (0.0, 0.0, 0.0)
   - AMBER is strictly OFF (0.0, 0.0, 0.0)
   - GREEN (Straight and/or Turn Arrows) is ON
2. AMBER:
   - RED is strictly OFF (0.0, 0.0, 0.0)
   - AMBER is ON (1.0, 0.7, 0.0)
   - GREEN is strictly OFF (0.0, 0.0, 0.0)
3. RED:
   - RED is ON (1.0, 0.0, 0.0)
   - AMBER is strictly OFF (0.0, 0.0, 0.0)
   - GREEN is strictly OFF (0.0, 0.0, 0.0)

Zero simultaneous glowing! Only ONE state is active at any moment per approach.
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

    RED_ON    = [1.0, 0.0, 0.0]
    RED_OFF   = [0.0, 0.0, 0.0]

    AMBER_ON  = [1.0, 0.7, 0.0]
    AMBER_OFF = [0.0, 0.0, 0.0]

    GREEN_ON  = [0.0, 1.0, 0.2]
    GREEN_OFF = [0.0, 0.0, 0.0]

    def set_approach(dir_name, state, left_arrow=False, right_arrow=False, straight=True):
        fields = emissive_fields.get(dir_name, {})
        if not fields:
            return
        
        if state == 'GREEN':
            if 'RED' in fields: fields['RED'].setSFColor(RED_OFF)
            if 'AMBER' in fields: fields['AMBER'].setSFColor(AMBER_OFF)
            if 'STRAIGHT' in fields: fields['STRAIGHT'].setSFColor(GREEN_ON if straight else GREEN_OFF)
            if 'LEFT' in fields: fields['LEFT'].setSFColor(GREEN_ON if left_arrow else GREEN_OFF)
            if 'RIGHT' in fields: fields['RIGHT'].setSFColor(GREEN_ON if right_arrow else GREEN_OFF)

        elif state == 'YELLOW':
            if 'RED' in fields: fields['RED'].setSFColor(RED_OFF)
            if 'AMBER' in fields: fields['AMBER'].setSFColor(AMBER_ON)
            if 'STRAIGHT' in fields: fields['STRAIGHT'].setSFColor(GREEN_OFF)
            if 'LEFT' in fields: fields['LEFT'].setSFColor(GREEN_OFF)
            if 'RIGHT' in fields: fields['RIGHT'].setSFColor(GREEN_OFF)

        elif state == 'RED':
            if 'RED' in fields: fields['RED'].setSFColor(RED_ON)
            if 'AMBER' in fields: fields['AMBER'].setSFColor(AMBER_OFF)
            if 'STRAIGHT' in fields: fields['STRAIGHT'].setSFColor(GREEN_OFF)
            if 'LEFT' in fields: fields['LEFT'].setSFColor(GREEN_OFF)
            if 'RIGHT' in fields: fields['RIGHT'].setSFColor(GREEN_OFF)

    TOTAL_CYCLE = 28.0

    while robot.step(timestep) != -1:
        sim_time = robot.getTime()
        cycle_t = sim_time % TOTAL_CYCLE

        if j_id == '41':
            # Junction 41 (Left End of Shortcut Parkway):
            # - 0-12s: North-South Main Road GREEN (South Straight+Right; North Straight+Left; East Shortcut Solid RED)
            # - 12-14s: North-South AMBER; East Shortcut Solid RED
            # - 14-26s: East Shortcut GREEN (Both Left & Right Turn Arrows GREEN; North & South Solid RED)
            # - 26-28s: East Shortcut AMBER; North & South Solid RED
            if cycle_t < 12.0:
                set_approach('SOUTH', 'GREEN', straight=True, right_arrow=True)
                set_approach('NORTH', 'GREEN', straight=True, left_arrow=True)
                set_approach('EAST',  'RED')
            elif cycle_t < 14.0:
                set_approach('SOUTH', 'YELLOW')
                set_approach('NORTH', 'YELLOW')
                set_approach('EAST',  'RED')
            elif cycle_t < 26.0:
                set_approach('SOUTH', 'RED')
                set_approach('NORTH', 'RED')
                set_approach('EAST',  'GREEN', straight=False, left_arrow=True, right_arrow=True)
            else:
                set_approach('SOUTH', 'RED')
                set_approach('NORTH', 'RED')
                set_approach('EAST',  'YELLOW')

        elif j_id == '43':
            # Junction 43 (Right End of Shortcut Parkway):
            # - 0-12s: North-South Main Road GREEN (South Straight+Left; North Straight+Right; West Shortcut Solid RED)
            # - 12-14s: North-South AMBER; West Shortcut Solid RED
            # - 14-26s: West Shortcut GREEN (Both Left & Right Turn Arrows GREEN; North & South Solid RED)
            # - 26-28s: West Shortcut AMBER; North & South Solid RED
            if cycle_t < 12.0:
                set_approach('SOUTH', 'GREEN', straight=True, left_arrow=True)
                set_approach('NORTH', 'GREEN', straight=True, right_arrow=True)
                set_approach('WEST',  'RED')
            elif cycle_t < 14.0:
                set_approach('SOUTH', 'YELLOW')
                set_approach('NORTH', 'YELLOW')
                set_approach('WEST',  'RED')
            elif cycle_t < 26.0:
                set_approach('SOUTH', 'RED')
                set_approach('NORTH', 'RED')
                set_approach('WEST',  'GREEN', straight=False, left_arrow=True, right_arrow=True)
            else:
                set_approach('SOUTH', 'RED')
                set_approach('NORTH', 'RED')
                set_approach('WEST',  'YELLOW')

        else:
            # 4-Way Standard Junctions (25, 26, 27)
            if j_id == '25':
                stage_sequence = ['EAST', 'NORTH', 'WEST', 'SOUTH']
            else:
                stage_sequence = ['SOUTH', 'EAST', 'NORTH', 'WEST']

            STAGE_LEN = 7.0
            GREEN_LEN = 5.0
            stage_idx = int(cycle_t // STAGE_LEN)
            stage_t = cycle_t % STAGE_LEN

            active_dir = stage_sequence[stage_idx]

            for d in directions:
                if d == active_dir:
                    if stage_t < GREEN_LEN:
                        set_approach(d, 'GREEN', straight=True, left_arrow=True, right_arrow=True)
                    else:
                        set_approach(d, 'YELLOW')
                else:
                    set_approach(d, 'RED')

if __name__ == '__main__':
    main()
