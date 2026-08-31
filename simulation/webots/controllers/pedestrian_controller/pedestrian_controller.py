"""
pedestrian_controller.py — Real-Time Crosswalk Pedestrian Supervisor in Webots.

Controls pedestrians crossing back and forth across zebra crossings at Junctions 25, 26, and 27.
Pedestrians walk at a natural pace (1.3 m/s), check both sides of the street, and smoothly oscillate across the crosswalk.
"""

import math
from controller import Supervisor

def main():
    robot = Supervisor()
    timestep = int(robot.getBasicTimeStep())
    if timestep <= 0:
        timestep = 32

    # Find all pedestrian nodes in the world
    ped_names = [
        "PED_J25_NORTH_1", "PED_J25_SOUTH_1", "PED_J25_EAST_1",
        "PED_J26_SOUTH_1", "PED_J26_NORTH_1", "PED_J26_WEST_1",
        "PED_J27_NORTH_1", "PED_J27_SOUTH_1"
    ]

    peds = []
    for name in ped_names:
        node = robot.getFromDef(name)
        if node:
            t_field = node.getField("translation")
            r_field = node.getField("rotation")
            if t_field:
                init_pos = t_field.getSFVec3f()
                peds.append({
                    'name': name,
                    'node': node,
                    't_field': t_field,
                    'r_field': r_field,
                    'init_pos': list(init_pos),
                    'axis': 'X' if ('NORTH' in name or 'SOUTH' in name) else 'Y',
                    'range': 18.0,
                    'speed': 1.25, # 1.25 m/s (~4.5 km/h natural walking pace)
                    'phase_offset': (len(peds) * 1.7)
                })

    print(f"Pedestrian Supervisor initialized with {len(peds)} active crosswalk pedestrians.")

    while robot.step(timestep) != -1:
        t = robot.getTime()

        for p in peds:
            # Triangular/Sinusoidal smooth crossing trajectory
            period = (p['range'] / p['speed']) * 2.0 # ~28.8 seconds to cross back & forth
            local_t = (t + p['phase_offset']) % period
            half = period / 2.0

            if local_t < half:
                progress = local_t / half # 0.0 -> 1.0 (crossing forward)
                forward = True
            else:
                progress = (period - local_t) / half # 1.0 -> 0.0 (crossing back)
                forward = False

            # Smooth ease-in-out movement
            smooth_prog = (1.0 - math.cos(progress * math.pi)) / 2.0
            offset = (smooth_prog - 0.5) * p['range']

            current_pos = list(p['init_pos'])
            if p['axis'] == 'X':
                current_pos[0] = p['init_pos'][0] + offset
                # Facing rotation: East (+X) or West (-X)
                if p['r_field']:
                    rot_angle = 1.5708 if forward else -1.5708
                    p['r_field'].setSFRotation([0, 0, 1, rot_angle])
            else:
                current_pos[1] = p['init_pos'][1] + offset
                # Facing rotation: North (+Y) or South (-Y)
                if p['r_field']:
                    rot_angle = 0.0 if forward else 3.14159
                    p['r_field'].setSFRotation([0, 0, 1, rot_angle])

            p['t_field'].setSFVec3f(current_pos)

if __name__ == '__main__':
    main()
