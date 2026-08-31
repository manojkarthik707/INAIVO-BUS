"""
traffic_light_controller.py — Real-Time 5-Aspect Indian Traffic Light Supervisor in Webots.

Directly drives PBR emissiveColor GPU shaders for:
- 🔴 Red Light
- 🟠 Amber / Orange Light
- ⬆️ Green Straight Arrow
- ⬅️ Green Left Arrow (24/7 Free Left on Red)
- ➡️ Green Right Arrow
"""

import sys
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

    # Discover and cache emissiveColor fields for all materials on this tower
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

    bound_count = sum(len(d) for d in emissive_fields.values())
    print(f"TrafficLight Supervisor for Junction {j_id} online: {bound_count} PBR emissive shaders bound.")

    # Colors:
    COLOR_RED_ON = [1.0, 0.05, 0.05]
    COLOR_RED_OFF = [0.08, 0.01, 0.01]

    COLOR_AMBER_ON = [1.0, 0.65, 0.05]
    COLOR_AMBER_OFF = [0.06, 0.03, 0.0]

    COLOR_GREEN_ON = [0.1, 1.0, 0.3]
    COLOR_GREEN_OFF = [0.0, 0.05, 0.01]

    # Standard 4-stage Indian actuated cycle:
    # Phase 0: North/South Green (14s)
    # Phase 1: North/South Yellow (2s)
    # Phase 2: East/West Green (14s)
    # Phase 3: East/West Yellow (2s)
    # Total cycle = 32s

    TOTAL_CYCLE = 32.0

    while robot.step(timestep) != -1:
        sim_time = robot.getTime()
        cycle_t = sim_time % TOTAL_CYCLE

        if cycle_t < 14.0:
            phase = 0 # North/South Green
        elif cycle_t < 16.0:
            phase = 1 # North/South Yellow
        elif cycle_t < 30.0:
            phase = 2 # East/West Green
        else:
            phase = 3 # East/West Yellow

        if phase == 0:
            # North/South Green
            for d in ['NORTH', 'SOUTH']:
                if 'RED' in emissive_fields[d]: emissive_fields[d]['RED'].setSFColor(COLOR_RED_OFF)
                if 'AMBER' in emissive_fields[d]: emissive_fields[d]['AMBER'].setSFColor(COLOR_AMBER_OFF)
                if 'STRAIGHT' in emissive_fields[d]: emissive_fields[d]['STRAIGHT'].setSFColor(COLOR_GREEN_ON)
                if 'LEFT' in emissive_fields[d]: emissive_fields[d]['LEFT'].setSFColor(COLOR_GREEN_ON)
                if 'RIGHT' in emissive_fields[d]: emissive_fields[d]['RIGHT'].setSFColor(COLOR_GREEN_ON)
            # East/West Red with 24/7 Free Left
            for d in ['EAST', 'WEST']:
                if 'RED' in emissive_fields[d]: emissive_fields[d]['RED'].setSFColor(COLOR_RED_ON)
                if 'AMBER' in emissive_fields[d]: emissive_fields[d]['AMBER'].setSFColor(COLOR_AMBER_OFF)
                if 'STRAIGHT' in emissive_fields[d]: emissive_fields[d]['STRAIGHT'].setSFColor(COLOR_GREEN_OFF)
                if 'LEFT' in emissive_fields[d]: emissive_fields[d]['LEFT'].setSFColor(COLOR_GREEN_ON) # 24/7 FREE LEFT
                if 'RIGHT' in emissive_fields[d]: emissive_fields[d]['RIGHT'].setSFColor(COLOR_GREEN_OFF)

        elif phase == 1:
            # North/South Yellow
            for d in ['NORTH', 'SOUTH']:
                if 'RED' in emissive_fields[d]: emissive_fields[d]['RED'].setSFColor(COLOR_RED_OFF)
                if 'AMBER' in emissive_fields[d]: emissive_fields[d]['AMBER'].setSFColor(COLOR_AMBER_ON)
                if 'STRAIGHT' in emissive_fields[d]: emissive_fields[d]['STRAIGHT'].setSFColor(COLOR_GREEN_OFF)
                if 'LEFT' in emissive_fields[d]: emissive_fields[d]['LEFT'].setSFColor(COLOR_GREEN_ON)
                if 'RIGHT' in emissive_fields[d]: emissive_fields[d]['RIGHT'].setSFColor(COLOR_GREEN_OFF)
            # East/West Red with Free Left
            for d in ['EAST', 'WEST']:
                if 'RED' in emissive_fields[d]: emissive_fields[d]['RED'].setSFColor(COLOR_RED_ON)
                if 'AMBER' in emissive_fields[d]: emissive_fields[d]['AMBER'].setSFColor(COLOR_AMBER_OFF)
                if 'STRAIGHT' in emissive_fields[d]: emissive_fields[d]['STRAIGHT'].setSFColor(COLOR_GREEN_OFF)
                if 'LEFT' in emissive_fields[d]: emissive_fields[d]['LEFT'].setSFColor(COLOR_GREEN_ON)
                if 'RIGHT' in emissive_fields[d]: emissive_fields[d]['RIGHT'].setSFColor(COLOR_GREEN_OFF)

        elif phase == 2:
            # East/West Green
            for d in ['EAST', 'WEST']:
                if 'RED' in emissive_fields[d]: emissive_fields[d]['RED'].setSFColor(COLOR_RED_OFF)
                if 'AMBER' in emissive_fields[d]: emissive_fields[d]['AMBER'].setSFColor(COLOR_AMBER_OFF)
                if 'STRAIGHT' in emissive_fields[d]: emissive_fields[d]['STRAIGHT'].setSFColor(COLOR_GREEN_ON)
                if 'LEFT' in emissive_fields[d]: emissive_fields[d]['LEFT'].setSFColor(COLOR_GREEN_ON)
                if 'RIGHT' in emissive_fields[d]: emissive_fields[d]['RIGHT'].setSFColor(COLOR_GREEN_ON)
            # North/South Red with Free Left
            for d in ['NORTH', 'SOUTH']:
                if 'RED' in emissive_fields[d]: emissive_fields[d]['RED'].setSFColor(COLOR_RED_ON)
                if 'AMBER' in emissive_fields[d]: emissive_fields[d]['AMBER'].setSFColor(COLOR_AMBER_OFF)
                if 'STRAIGHT' in emissive_fields[d]: emissive_fields[d]['STRAIGHT'].setSFColor(COLOR_GREEN_OFF)
                if 'LEFT' in emissive_fields[d]: emissive_fields[d]['LEFT'].setSFColor(COLOR_GREEN_ON)
                if 'RIGHT' in emissive_fields[d]: emissive_fields[d]['RIGHT'].setSFColor(COLOR_GREEN_OFF)

        elif phase == 3:
            # East/West Yellow
            for d in ['EAST', 'WEST']:
                if 'RED' in emissive_fields[d]: emissive_fields[d]['RED'].setSFColor(COLOR_RED_OFF)
                if 'AMBER' in emissive_fields[d]: emissive_fields[d]['AMBER'].setSFColor(COLOR_AMBER_ON)
                if 'STRAIGHT' in emissive_fields[d]: emissive_fields[d]['STRAIGHT'].setSFColor(COLOR_GREEN_OFF)
                if 'LEFT' in emissive_fields[d]: emissive_fields[d]['LEFT'].setSFColor(COLOR_GREEN_ON)
                if 'RIGHT' in emissive_fields[d]: emissive_fields[d]['RIGHT'].setSFColor(COLOR_GREEN_OFF)
            # North/South Red with Free Left
            for d in ['NORTH', 'SOUTH']:
                if 'RED' in emissive_fields[d]: emissive_fields[d]['RED'].setSFColor(COLOR_RED_ON)
                if 'AMBER' in emissive_fields[d]: emissive_fields[d]['AMBER'].setSFColor(COLOR_AMBER_OFF)
                if 'STRAIGHT' in emissive_fields[d]: emissive_fields[d]['STRAIGHT'].setSFColor(COLOR_GREEN_OFF)
                if 'LEFT' in emissive_fields[d]: emissive_fields[d]['LEFT'].setSFColor(COLOR_GREEN_ON)
                if 'RIGHT' in emissive_fields[d]: emissive_fields[d]['RIGHT'].setSFColor(COLOR_GREEN_OFF)

if __name__ == '__main__':
    main()
