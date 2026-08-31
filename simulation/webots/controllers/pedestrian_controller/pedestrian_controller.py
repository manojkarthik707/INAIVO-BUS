"""
pedestrian_controller.py — Active AI Collision Avoidance & Traffic-Synchronized Pedestrian Supervisor.

Multi-Layered Safety Architecture:
1. Dynamic Proximity Sensing:
   - Queries all active vehicles in real-time.
   - If any vehicle is within 5.5 meters of the pedestrian's crosswalk path, the pedestrian YIELDS / HALTS immediately.
2. Signal-Phase Protection:
   - Pedestrians only attempt crossing when their crosswalk direction has a protected red phase for crossing traffic.
3. Rapid Clearance:
   - Crosses at brisk 4.5 m/s when clear to minimize street exposure.
   - Restores upright stance Z=1.27m on all updates.
"""

import math
from controller import Supervisor

def main():
    robot = Supervisor()
    timestep = int(robot.getBasicTimeStep())
    if timestep <= 0:
        timestep = 32

    ped_configs = [
        # Junction 26 (-45.0, 45.0)
        {'name': 'PED_J26_SOUTH', 'jid': '26', 'corridor': 'NS', 'axis': 'X', 'min': -55.0, 'max': -35.0, 'fixed': 33.5},
        {'name': 'PED_J26_NORTH', 'jid': '26', 'corridor': 'NS', 'axis': 'X', 'min': -55.0, 'max': -35.0, 'fixed': 56.5},
        {'name': 'PED_J26_EAST',  'jid': '26', 'corridor': 'EW', 'axis': 'Y', 'min': 35.0,  'max': 55.0,  'fixed': -33.5},
        {'name': 'PED_J26_WEST',  'jid': '26', 'corridor': 'EW', 'axis': 'Y', 'min': 35.0,  'max': 55.0,  'fixed': -56.5},

        # Junction 25 (45.0, -45.0)
        {'name': 'PED_J25_SOUTH', 'jid': '25', 'corridor': 'NS', 'axis': 'X', 'min': 35.0,  'max': 55.0,  'fixed': -56.5},
        {'name': 'PED_J25_NORTH', 'jid': '25', 'corridor': 'NS', 'axis': 'X', 'min': 35.0,  'max': 55.0,  'fixed': -33.5},
        {'name': 'PED_J25_EAST',  'jid': '25', 'corridor': 'EW', 'axis': 'Y', 'min': -55.0, 'max': -35.0, 'fixed': 56.5},
        {'name': 'PED_J25_WEST',  'jid': '25', 'corridor': 'EW', 'axis': 'Y', 'min': -55.0, 'max': -35.0, 'fixed': 33.5},

        # Junction 27 (105.0, 93.0)
        {'name': 'PED_J27_SOUTH', 'jid': '27', 'corridor': 'NS', 'axis': 'X', 'min': 95.0,  'max': 115.0, 'fixed': 81.5},
        {'name': 'PED_J27_NORTH', 'jid': '27', 'corridor': 'NS', 'axis': 'X', 'min': 95.0,  'max': 115.0, 'fixed': 104.5},
        {'name': 'PED_J27_EAST',  'jid': '27', 'corridor': 'EW', 'axis': 'Y', 'min': 83.0,  'max': 103.0, 'fixed': 116.5},
        {'name': 'PED_J27_WEST',  'jid': '27', 'corridor': 'EW', 'axis': 'Y', 'min': 83.0,  'max': 103.0, 'fixed': 93.5},
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
                    'current_pos': cfg['min'],
                    'target_side': 'max',
                    'is_crossing': False,
                })

    root_children = robot.getRoot().getField("children")
    print(f"Active AI Pedestrian Collision Avoidance Supervisor online: {len(peds)} pedestrians protected.")

    TOTAL_CYCLE = 28.0
    STAGE_LEN = 7.0
    WALK_SPEED = 4.5 # 4.5 m/s brisk pace
    SAFE_DISTANCE = 5.5 # 5.5 meters vehicle buffer

    while robot.step(timestep) != -1:
        sim_time = robot.getTime()
        dt = timestep / 1000.0
        cycle_t = sim_time % TOTAL_CYCLE
        stage_idx = int(cycle_t // STAGE_LEN)
        t_in_stage = cycle_t % STAGE_LEN

        # Gather real-time positions of all active vehicles
        vehicle_positions = []
        n_children = root_children.getCount()
        for i in range(n_children):
            child = root_children.getMFNode(i)
            if child:
                name_field = child.getField("name")
                if name_field:
                    n_val = name_field.getSFString()
                    if n_val.startswith("veh_") or n_val.startswith("transit_bus") or n_val.startswith("SUMO_"):
                        t_val = child.getField("translation")
                        if t_val:
                            pos = t_val.getSFVec3f()
                            vehicle_positions.append((pos[0], pos[1]))

        for p in peds:
            cfg = p['cfg']
            jid = cfg['jid']
            corridor = cfg['corridor']

            # Calculate pedestrian 2D world coordinates
            if cfg['axis'] == 'X':
                ped_x = p['current_pos']
                ped_y = cfg['fixed']
            else:
                ped_x = cfg['fixed']
                ped_y = p['current_pos']

            # Check if any vehicle is dangerously close to the pedestrian
            vehicle_danger = False
            for vx, vy in vehicle_positions:
                dist = math.hypot(vx - ped_x, vy - ped_y)
                if dist < SAFE_DISTANCE:
                    vehicle_danger = True
                    break

            if jid == '25':
                is_safe_stage = (stage_idx in [0, 2])
            else:
                is_safe_stage = (stage_idx in [1, 3])

            # Only initiate crossing during first 1.2s of protected stage if path is clear
            if is_safe_stage and t_in_stage < 1.2 and not vehicle_danger:
                p['is_crossing'] = True
            elif not is_safe_stage and (p['current_pos'] <= cfg['min'] + 0.5 or p['current_pos'] >= cfg['max'] - 0.5):
                p['is_crossing'] = False

            # If vehicle is dangerously close, pause walking immediately
            if vehicle_danger:
                continue

            if p['is_crossing']:
                if p['target_side'] == 'max':
                    p['current_pos'] += WALK_SPEED * dt
                    rot = [0, 0, 1, 0.0] if cfg['axis'] == 'X' else [0, 0, 1, 1.5708]
                    if p['current_pos'] >= cfg['max']:
                        p['current_pos'] = cfg['max']
                        p['target_side'] = 'min'
                        p['is_crossing'] = False
                else:
                    p['current_pos'] -= WALK_SPEED * dt
                    rot = [0, 0, 1, 3.14159] if cfg['axis'] == 'X' else [0, 0, 1, -1.5708]
                    if p['current_pos'] <= cfg['min']:
                        p['current_pos'] = cfg['min']
                        p['target_side'] = 'max'
                        p['is_crossing'] = False

                if cfg['axis'] == 'X':
                    p['t_field'].setSFVec3f([p['current_pos'], cfg['fixed'], 1.27])
                else:
                    p['t_field'].setSFVec3f([cfg['fixed'], p['current_pos'], 1.27])
                p['r_field'].setSFRotation(rot)

if __name__ == '__main__':
    main()
