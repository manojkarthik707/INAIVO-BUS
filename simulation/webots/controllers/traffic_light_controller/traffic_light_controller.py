"""
traffic_light_controller.py — Millisecond-Synchronized Indian Traffic Signal Supervisor.

Exact 28.0s Cycle Synchronization with SUMO:
- Junctions 25, 26, 27 (4-Way):
  * Stage 0 (0-5s Green, 5-7s Amber): Active Direction 1
  * Stage 1 (7-12s Green, 12-14s Amber): Active Direction 2
  * Stage 2 (14-19s Green, 19-21s Amber): Active Direction 3
  * Stage 3 (21-26s Green, 26-28s Amber): Active Direction 4
- Junctions 41, 43 (3-Way Shortcut):
  * Stage 0 (0-12s Green, 12-14s Amber): Main Road Green, Shortcut Road Solid Red
  * Stage 1 (14-26s Green, 26-28s Amber): Shortcut Road Green, Main Road Solid Red
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
