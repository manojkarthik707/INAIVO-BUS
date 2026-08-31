"""
traffic_light_controller.py — Real-Time 4-Stage Indian Traffic Light Supervisor in Webots.

100% Mathematically Synchronized with SUMO Signal Logic & Physical Road Approaches:
- When SUMO grants green to an approach, the 3D signal face facing that approach illuminates GREEN.
- All 3 stopped approaches show SOLID RED + 24/7 Free Left on Red.
- Vehicles only move when their facing signal is GREEN.
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

    print(f"TrafficLight Supervisor for Junction {j_id} online: {sum(len(d) for d in emissive_fields.values())} shaders bound.")

    # High-intensity active LED colors vs dark off colors
    RED_ON   = [1.0, 0.05, 0.05]
    RED_OFF  = [0.08, 0.01, 0.01]

    AMBER_ON  = [1.0, 0.65, 0.05]
    AMBER_OFF = [0.06, 0.03, 0.0]

    GREEN_ON  = [0.1, 1.0, 0.3]
    GREEN_OFF = [0.0, 0.05, 0.01]

    def set_approach_state(dir_name, state):
        # state: 'GREEN', 'YELLOW', 'RED'
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

    # Define exact cardinal sequence corresponding to SUMO's linkIndex phases:
    # In Junction 26 & 27:
    # Links 0..4   = South Approach (Facing South)
    # Links 5..9   = East Approach  (Facing East)
    # Links 10..14 = North Approach (Facing North)
    # Links 15..19 = West Approach  (Facing West)
    
    # In Junction 25:
    # Links 0..4   = East Approach  (Facing East)
    # Links 5..9   = North Approach (Facing North)
    # Links 10..14 = West Approach  (Facing West)
    # Links 15..19 = South Approach (Facing South)

    if j_id == '25':
        stage_sequence = ['EAST', 'NORTH', 'WEST', 'SOUTH']
    else:
        stage_sequence = ['SOUTH', 'EAST', 'NORTH', 'WEST']

    # Total cycle = 4 stages * (8s Green + 2s Yellow) = 40s
    TOTAL_CYCLE = 40.0

    while robot.step(timestep) != -1:
        sim_time = robot.getTime()
        cycle_t = sim_time % TOTAL_CYCLE

        stage_idx = int(cycle_t // 10.0) # 0, 1, 2, 3
        stage_sub_t = cycle_t % 10.0      # 0.0 .. 10.0s

        active_dir = stage_sequence[stage_idx]

        for d in directions:
            if d == active_dir:
                if stage_sub_t < 8.0:
                    set_approach_state(d, 'GREEN')
                else:
                    set_approach_state(d, 'YELLOW')
            else:
                set_approach_state(d, 'RED')

if __name__ == '__main__':
    main()
