"""
traffic_light_controller.py — Real-Time 4-Way Indian Traffic Light Supervisor in Webots.

Synchronizes the 4-way traffic light towers at Junctions 25, 26, 27 with:
- Red Light
- Amber / Orange Light
- Green Straight Arrow
- Green Left Arrow (24/7 Free Left on Red)
- Green Right Arrow
"""

import time
import math
from controller import Supervisor

def main():
    robot = Supervisor()
    timestep = int(robot.getBasicTimeStep())
    if timestep <= 0:
        timestep = 32

    junctions = ['25', '26', '27']
    directions = ['north', 'south', 'east', 'west']
    aspects = ['red', 'amber', 'straight', 'left', 'right']

    # Discover all LED devices
    leds = {}
    for j in junctions:
        leds[j] = {}
        for d in directions:
            leds[j][d] = {}
            for a in aspects:
                name = f"tl{j}_{d}_{a}"
                device = robot.getDevice(name)
                if device:
                    leds[j][d][a] = device

    print(f"TrafficLight Supervisor initialized with {sum(len(d) for j in leds.values() for d in j.values())} active LED devices.")

    # Standard cycle timing:
    # Phase 0: North/South Green (14s)
    # Phase 1: North/South Yellow (2s)
    # Phase 2: East/West Green (14s)
    # Phase 3: East/West Yellow (2s)
    # Total cycle = 32s

    PHASE_DURS = [14.0, 2.0, 14.0, 2.0]
    TOTAL_CYCLE = sum(PHASE_DURS)

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

        for j in junctions:
            # Handle North & South
            if phase == 0:
                # North/South Green
                for d in ['north', 'south']:
                    if 'red' in leds[j][d]: leds[j][d]['red'].set(0)
                    if 'amber' in leds[j][d]: leds[j][d]['amber'].set(0)
                    if 'straight' in leds[j][d]: leds[j][d]['straight'].set(1)
                    if 'left' in leds[j][d]: leds[j][d]['left'].set(1)
                    if 'right' in leds[j][d]: leds[j][d]['right'].set(1)
                # East/West Red with 24/7 Free Left
                for d in ['east', 'west']:
                    if 'red' in leds[j][d]: leds[j][d]['red'].set(1)
                    if 'amber' in leds[j][d]: leds[j][d]['amber'].set(0)
                    if 'straight' in leds[j][d]: leds[j][d]['straight'].set(0)
                    if 'left' in leds[j][d]: leds[j][d]['left'].set(1) # FREE LEFT ON RED
                    if 'right' in leds[j][d]: leds[j][d]['right'].set(0)

            elif phase == 1:
                # North/South Yellow
                for d in ['north', 'south']:
                    if 'red' in leds[j][d]: leds[j][d]['red'].set(0)
                    if 'amber' in leds[j][d]: leds[j][d]['amber'].set(1)
                    if 'straight' in leds[j][d]: leds[j][d]['straight'].set(0)
                    if 'left' in leds[j][d]: leds[j][d]['left'].set(1)
                    if 'right' in leds[j][d]: leds[j][d]['right'].set(0)
                # East/West Red with Free Left
                for d in ['east', 'west']:
                    if 'red' in leds[j][d]: leds[j][d]['red'].set(1)
                    if 'amber' in leds[j][d]: leds[j][d]['amber'].set(0)
                    if 'straight' in leds[j][d]: leds[j][d]['straight'].set(0)
                    if 'left' in leds[j][d]: leds[j][d]['left'].set(1) # FREE LEFT ON RED
                    if 'right' in leds[j][d]: leds[j][d]['right'].set(0)

            elif phase == 2:
                # East/West Green
                for d in ['east', 'west']:
                    if 'red' in leds[j][d]: leds[j][d]['red'].set(0)
                    if 'amber' in leds[j][d]: leds[j][d]['amber'].set(0)
                    if 'straight' in leds[j][d]: leds[j][d]['straight'].set(1)
                    if 'left' in leds[j][d]: leds[j][d]['left'].set(1)
                    if 'right' in leds[j][d]: leds[j][d]['right'].set(1)
                # North/South Red with Free Left
                for d in ['north', 'south']:
                    if 'red' in leds[j][d]: leds[j][d]['red'].set(1)
                    if 'amber' in leds[j][d]: leds[j][d]['amber'].set(0)
                    if 'straight' in leds[j][d]: leds[j][d]['straight'].set(0)
                    if 'left' in leds[j][d]: leds[j][d]['left'].set(1) # FREE LEFT ON RED
                    if 'right' in leds[j][d]: leds[j][d]['right'].set(0)

            elif phase == 3:
                # East/West Yellow
                for d in ['east', 'west']:
                    if 'red' in leds[j][d]: leds[j][d]['red'].set(0)
                    if 'amber' in leds[j][d]: leds[j][d]['amber'].set(1)
                    if 'straight' in leds[j][d]: leds[j][d]['straight'].set(0)
                    if 'left' in leds[j][d]: leds[j][d]['left'].set(1)
                    if 'right' in leds[j][d]: leds[j][d]['right'].set(0)
                # North/South Red with Free Left
                for d in ['north', 'south']:
                    if 'red' in leds[j][d]: leds[j][d]['red'].set(1)
                    if 'amber' in leds[j][d]: leds[j][d]['amber'].set(0)
                    if 'straight' in leds[j][d]: leds[j][d]['straight'].set(0)
                    if 'left' in leds[j][d]: leds[j][d]['left'].set(1) # FREE LEFT ON RED
                    if 'right' in leds[j][d]: leds[j][d]['right'].set(0)

if __name__ == '__main__':
    main()
