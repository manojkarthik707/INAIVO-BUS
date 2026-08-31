"""
traffic_light_controller.py — Real-Time 4-Way Indian Traffic Light Supervisor in Webots.

Controls the 4-faced central traffic light towers at Junctions 25, 26, 27:
- Red Light (Top)
- Amber Light (Middle)
- Green Straight Arrow (Lower)
- Green Left Arrow (24/7 Free Left on Red)
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

    directions = ['north', 'south', 'east', 'west']
    aspects = ['red', 'amber', 'straight', 'left']

    # Discover all LED devices on this specific junction tower
    leds = {}
    for d in directions:
        leds[d] = {}
        for a in aspects:
            name = f"tl{j_id}_{d}_{a}"
            device = robot.getDevice(name)
            if device:
                leds[d][a] = device

    found_count = sum(len(d) for d in leds.values())
    print(f"TrafficLight Supervisor for Junction {j_id} online ({found_count} LED devices bound).")

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
            # North/South Green (Straight ON, Free Left ON, Red/Amber OFF)
            for d in ['north', 'south']:
                if 'red' in leds[d]: leds[d]['red'].set(0)
                if 'amber' in leds[d]: leds[d]['amber'].set(0)
                if 'straight' in leds[d]: leds[d]['straight'].set(1)
                if 'left' in leds[d]: leds[d]['left'].set(1)
            # East/West Red (Red ON, Free Left ON, Amber/Straight OFF)
            for d in ['east', 'west']:
                if 'red' in leds[d]: leds[d]['red'].set(1)
                if 'amber' in leds[d]: leds[d]['amber'].set(0)
                if 'straight' in leds[d]: leds[d]['straight'].set(0)
                if 'left' in leds[d]: leds[d]['left'].set(1) # 24/7 FREE LEFT

        elif phase == 1:
            # North/South Yellow (Amber ON, Straight OFF, Free Left ON)
            for d in ['north', 'south']:
                if 'red' in leds[d]: leds[d]['red'].set(0)
                if 'amber' in leds[d]: leds[d]['amber'].set(1)
                if 'straight' in leds[d]: leds[d]['straight'].set(0)
                if 'left' in leds[d]: leds[d]['left'].set(1)
            # East/West Red (Red ON, Free Left ON)
            for d in ['east', 'west']:
                if 'red' in leds[d]: leds[d]['red'].set(1)
                if 'amber' in leds[d]: leds[d]['amber'].set(0)
                if 'straight' in leds[d]: leds[d]['straight'].set(0)
                if 'left' in leds[d]: leds[d]['left'].set(1)

        elif phase == 2:
            # East/West Green (Straight ON, Free Left ON, Red/Amber OFF)
            for d in ['east', 'west']:
                if 'red' in leds[d]: leds[d]['red'].set(0)
                if 'amber' in leds[d]: leds[d]['amber'].set(0)
                if 'straight' in leds[d]: leds[d]['straight'].set(1)
                if 'left' in leds[d]: leds[d]['left'].set(1)
            # North/South Red (Red ON, Free Left ON)
            for d in ['north', 'south']:
                if 'red' in leds[d]: leds[d]['red'].set(1)
                if 'amber' in leds[d]: leds[d]['amber'].set(0)
                if 'straight' in leds[d]: leds[d]['straight'].set(0)
                if 'left' in leds[d]: leds[d]['left'].set(1)

        elif phase == 3:
            # East/West Yellow (Amber ON, Straight OFF, Free Left ON)
            for d in ['east', 'west']:
                if 'red' in leds[d]: leds[d]['red'].set(0)
                if 'amber' in leds[d]: leds[d]['amber'].set(1)
                if 'straight' in leds[d]: leds[d]['straight'].set(0)
                if 'left' in leds[d]: leds[d]['left'].set(1)
            # North/South Red (Red ON, Free Left ON)
            for d in ['north', 'south']:
                if 'red' in leds[d]: leds[d]['red'].set(1)
                if 'amber' in leds[d]: leds[d]['amber'].set(0)
                if 'straight' in leds[d]: leds[d]['straight'].set(0)
                if 'left' in leds[d]: leds[d]['left'].set(1)

if __name__ == '__main__':
    main()
