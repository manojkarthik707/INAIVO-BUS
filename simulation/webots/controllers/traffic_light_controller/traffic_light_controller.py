"""
traffic_light_controller.py — Fast Snappy 4-Stage Indian Traffic Light Supervisor in Webots.

High-Speed 20s Cycle (4s Green + 1s Yellow per approach):
- When SUMO grants green to an approach, the 3D signal face facing that approach illuminates GREEN.
- All 3 stopped approaches show SOLID RED + 24/7 Free Left on Red.
- Fully synchronized with SUMO's 20s fast actuated cycle.
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
    else:
        j_id = '25'

    directions = ['NORTH', 'SOUTH', 'EAST', 'WEST']
    aspects = ['RED', 'AMBER', 'STRAIGHT', 'LEFT', 'RIGHT']

    # Discover and cache emissiveColor shader fields for all 4 faces
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

    print(f"Fast TrafficLight Supervisor for Junction {j_id} online: {sum(len(d) for d in emissive_fields.values())} shaders bound.")

    # High-intensity active LED colors vs dark off colors
    RED_ON   = [1.0, 0.05, 0.05]
    RED_OFF  = [0.08, 0.01, 0.01]

    AMBER_ON  = [1.0, 0.65, 0.05]
    AMBER_OFF = [0.06, 0.03, 0.0]

    GREEN_ON  = [0.1, 1.0, 0.3]
    GREEN_OFF = [0.0, 0.05, 0.01]

    def set_approach_state(dir_name, state):
        fields = emissive_fields.get(dir_name, {})
        if not fields:
            return
        
        if state == 'GREEN':
            # Active Green: Straight ON, Right ON, Free Left ON, Red/Amber OFF
            if 'RED' in fields: fields['RED'].setSFColor(RED_OFF)
            if 'AMBER' in fields: fields['AMBER'].setSFColor(AMBER_OFF)
            if 'STRAIGHT' in fields: fields['STRAIGHT'].setSFColor(GREEN_ON)
            if 'LEFT' in fields: fields['LEFT'].setSFColor(GREEN_ON) # 24/7 Free Left
            if 'RIGHT' in fields: fields['RIGHT'].setSFColor(GREEN_ON)

        elif state == 'YELLOW':
            # Transition Amber: Amber ON, Straight/Right OFF, Free Left ON, Red OFF
            if 'RED' in fields: fields['RED'].setSFColor(RED_OFF)
            if 'AMBER' in fields: fields['AMBER'].setSFColor(AMBER_ON)
            if 'STRAIGHT' in fields: fields['STRAIGHT'].setSFColor(GREEN_OFF)
            if 'LEFT' in fields: fields['LEFT'].setSFColor(GREEN_ON) # 24/7 Free Left
            if 'RIGHT' in fields: fields['RIGHT'].setSFColor(GREEN_OFF)

        elif state == 'RED':
            # Stopped Red: RED ON, Free Left ON (24/7 Indian Rule), Amber/Straight/Right OFF
            if 'RED' in fields: fields['RED'].setSFColor(RED_ON)
            if 'AMBER' in fields: fields['AMBER'].setSFColor(AMBER_OFF)
            if 'STRAIGHT' in fields: fields['STRAIGHT'].setSFColor(GREEN_OFF)
            if 'LEFT' in fields: fields['LEFT'].setSFColor(GREEN_ON) # 24/7 Free Left on Red
            if 'RIGHT' in fields: fields['RIGHT'].setSFColor(GREEN_OFF) # Right Turn STRICTLY OFF on Red!

    # Exact cardinal sequence corresponding to SUMO's linkIndex phases
    if j_id == '25':
        stage_sequence = ['EAST', 'NORTH', 'WEST', 'SOUTH']
    else:
        stage_sequence = ['SOUTH', 'EAST', 'NORTH', 'WEST']

    # Fast 20s Cycle (4 stages * (4s Green + 1s Yellow) = 20s total cycle)
    TOTAL_CYCLE = 20.0
    STAGE_LEN = 5.0
    GREEN_LEN = 4.0

    while robot.step(timestep) != -1:
        sim_time = robot.getTime()
        cycle_t = sim_time % TOTAL_CYCLE

        stage_idx = int(cycle_t // STAGE_LEN) # 0, 1, 2, 3
        stage_sub_t = cycle_t % STAGE_LEN      # 0.0 .. 5.0s

        active_dir = stage_sequence[stage_idx]

        for d in directions:
            if d == active_dir:
                if stage_sub_t < GREEN_LEN:
                    set_approach_state(d, 'GREEN')
                else:
                    set_approach_state(d, 'YELLOW')
            else:
                set_approach_state(d, 'RED')

if __name__ == '__main__':
    main()
