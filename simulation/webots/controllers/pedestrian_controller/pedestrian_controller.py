"""
pedestrian_controller.py — Signal-Obedient Crosswalk Pedestrian Supervisor in Webots.

Pedestrian Traffic Rules:
1. When vehicular traffic on an approach has GREEN / YELLOW, pedestrians WAIT SAFELY on the sidewalk curb.
2. When vehicular traffic on an approach turns RED, pedestrians WALK PROMPTLY across the zebra crossing to the other side.
3. Pedestrians walk at a natural pace (1.3 m/s), face the exact direction of travel, and turn around upon reaching the opposite curb.
"""

import math
from controller import Supervisor

def main():
    robot = Supervisor()
    timestep = int(robot.getBasicTimeStep())
    if timestep <= 0:
        timestep = 32

    # Configuration for all 12 crossing pedestrians:
    # (name, junction_id, approach_dir, walk_axis, min_coord, max_coord, fixed_coord)
    ped_configs = [
        # Junction 26
        {'name': 'PED_J26_SOUTH', 'jid': '26', 'dir': 'SOUTH', 'axis': 'X', 'min': -55.0, 'max': -35.0, 'fixed': 33.5},
        {'name': 'PED_J26_NORTH', 'jid': '26', 'dir': 'NORTH', 'axis': 'X', 'min': -55.0, 'max': -35.0, 'fixed': 56.5},
        {'name': 'PED_J26_EAST',  'jid': '26', 'dir': 'EAST',  'axis': 'Y', 'min': 35.0,  'max': 55.0,  'fixed': -33.5},
        {'name': 'PED_J26_WEST',  'jid': '26', 'dir': 'WEST',  'axis': 'Y', 'min': 35.0,  'max': 55.0,  'fixed': -56.5},

        # Junction 25
        {'name': 'PED_J25_SOUTH', 'jid': '25', 'dir': 'SOUTH', 'axis': 'X', 'min': 35.0,  'max': 55.0,  'fixed': -56.5},
        {'name': 'PED_J25_NORTH', 'jid': '25', 'dir': 'NORTH', 'axis': 'X', 'min': 35.0,  'max': 55.0,  'fixed': -33.5},
        {'name': 'PED_J25_EAST',  'jid': '25', 'dir': 'EAST',  'axis': 'Y', 'min': -55.0, 'max': -35.0, 'fixed': 56.5},
        {'name': 'PED_J25_WEST',  'jid': '25', 'dir': 'WEST',  'axis': 'Y', 'min': -55.0, 'max': -35.0, 'fixed': 33.5},

        # Junction 27
        {'name': 'PED_J27_SOUTH', 'jid': '27', 'dir': 'SOUTH', 'axis': 'X', 'min': 95.0,  'max': 115.0, 'fixed': 81.5},
        {'name': 'PED_J27_NORTH', 'jid': '27', 'dir': 'NORTH', 'axis': 'X', 'min': 95.0,  'max': 115.0, 'fixed': 104.5},
        {'name': 'PED_J27_EAST',  'jid': '27', 'dir': 'EAST',  'axis': 'Y', 'min': 83.0,  'max': 103.0, 'fixed': 116.5},
        {'name': 'PED_J27_WEST',  'jid': '27', 'dir': 'WEST',  'axis': 'Y', 'min': 83.0,  'max': 103.0, 'fixed': 93.5},
    ]

    peds = []
    for cfg in ped_configs:
        node = robot.getFromDef(cfg['name'])
        if node:
            t_field = node.getField("translation")
            r_field = node.getField("rotation")
            if t_field and r_field:
                peds.append({
                    'cfg': cfg,
                    't_field': t_field,
                    'r_field': r_field,
                    'current_pos': cfg['min'], # Start on min curb
                    'target_side': 'max',      # Headed to max curb
                    'state': 'WAITING',        # 'WAITING' or 'CROSSING'
                })

    print(f"Pedestrian Controller online: {len(peds)} pedestrians bound to traffic signals.")

    TOTAL_CYCLE = 28.0
    STAGE_LEN = 7.0

    # Walking speed = 1.4 m/s (~5 km/h standard brisk walk across 20m road = 14.2s walk)
    WALK_SPEED = 1.4

    while robot.step(timestep) != -1:
        sim_time = robot.getTime()
        dt = timestep / 1000.0
        cycle_t = sim_time % TOTAL_CYCLE
        stage_idx = int(cycle_t // STAGE_LEN)

        for p in peds:
            cfg = p['cfg']
            jid = cfg['jid']

            # Determine active vehicular direction (which approach has green)
            if jid == '25':
                active_veh_dir = ['EAST', 'NORTH', 'WEST', 'SOUTH'][stage_idx]
            else:
                active_veh_dir = ['SOUTH', 'EAST', 'NORTH', 'WEST'][stage_idx]

            # Pedestrian CAN WALK if vehicular traffic on this approach is RED!
            # If active_veh_dir == cfg['dir'], cars are moving -> Pedestrian MUST WAIT!
            can_walk = (active_veh_dir != cfg['dir'])

            if can_walk:
                # Pedestrian crosses towards target side
                if p['target_side'] == 'max':
                    p['current_pos'] += WALK_SPEED * dt
                    # Face in positive direction
                    if cfg['axis'] == 'X':
                        p['r_field'].setSFRotation([0, 0, 1, 1.5708]) # Face East (+X)
                    else:
                        p['r_field'].setSFRotation([0, 0, 1, 0.0])    # Face North (+Y)

                    if p['current_pos'] >= cfg['max']:
                        p['current_pos'] = cfg['max']
                        p['target_side'] = 'min' # Reached far curb, next trip goes back
                else:
                    p['current_pos'] -= WALK_SPEED * dt
                    # Face in negative direction
                    if cfg['axis'] == 'X':
                        p['r_field'].setSFRotation([0, 0, 1, -1.5708]) # Face West (-X)
                    else:
                        p['r_field'].setSFRotation([0, 0, 1, 3.14159]) # Face South (-Y)

                    if p['current_pos'] <= cfg['min']:
                        p['current_pos'] = cfg['min']
                        p['target_side'] = 'max' # Reached starting curb
            else:
                # Cars have Green: If pedestrian is on curb, wait safely on sidewalk
                # If caught mid-crossing, briskly clear the crosswalk to the nearest curb
                if p['current_pos'] > cfg['min'] and p['current_pos'] < cfg['max']:
                    # Finish clearing to the intended target curb
                    if p['target_side'] == 'max':
                        p['current_pos'] += WALK_SPEED * 1.2 * dt
                        if p['current_pos'] >= cfg['max']:
                            p['current_pos'] = cfg['max']
                            p['target_side'] = 'min'
                    else:
                        p['current_pos'] -= WALK_SPEED * 1.2 * dt
                        if p['current_pos'] <= cfg['min']:
                            p['current_pos'] = cfg['min']
                            p['target_side'] = 'max'

            # Apply 3D coordinate
            if cfg['axis'] == 'X':
                p['t_field'].setSFVec3f([p['current_pos'], cfg['fixed'], 1.27])
            else:
                p['t_field'].setSFVec3f([cfg['fixed'], p['current_pos'], 1.27])

if __name__ == '__main__':
    main()
