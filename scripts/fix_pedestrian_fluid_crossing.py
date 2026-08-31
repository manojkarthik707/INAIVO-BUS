PED_PATH = r"f:\VEHDEMO\simulation\webots\controllers\pedestrian_controller\pedestrian_controller.py"

ped_code = """\"\"\"
pedestrian_controller.py — Fluid, Protected Pedestrian Crosswalk Supervisor.

Robust Logic:
1. Signal-Phase Synchronization:
   - Pedestrians initiate crossing when vehicular cross-traffic is stopped on RED.
2. Fluid Non-Stop Crossing:
   - Once a pedestrian begins crossing, they walk smoothly and continuously to the opposite sidewalk without freezing in the road.
   - Stopped vehicles at red lights behind the stop line do not block pedestrians.
3. Rapid Pace (4.5 m/s):
   - Clears the street in ~3.8 seconds, well before the vehicular signal turns green.
4. Correct Elevation (Z = 1.27m):
   - Keeps feet firmly on the asphalt with animated walking legs.
\"\"\"

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

    print(f"Fluid Protected Pedestrian Supervisor online: {len(peds)} pedestrians active.")

    TOTAL_CYCLE = 28.0
    STAGE_LEN = 7.0
    WALK_SPEED = 4.5 # 4.5 m/s brisk pace -> crosses 18m street in 4.0 seconds

    while robot.step(timestep) != -1:
        sim_time = robot.getTime()
        dt = timestep / 1000.0
        cycle_t = sim_time % TOTAL_CYCLE
        stage_idx = int(cycle_t // STAGE_LEN)
        t_in_stage = cycle_t % STAGE_LEN

        for p in peds:
            cfg = p['cfg']
            jid = cfg['jid']
            corridor = cfg['corridor']

            # Safe stages: Crossing occurs when cross-traffic approach is on protected RED
            if jid == '25':
                is_safe_stage = (stage_idx in [0, 2])
            else:
                is_safe_stage = (stage_idx in [1, 3])

            # Initiate crossing during first 1.2s of the safe stage
            if is_safe_stage and t_in_stage < 1.2 and not p['is_crossing']:
                # Only initiate if currently waiting on the sidewalk curb
                if p['current_pos'] <= cfg['min'] + 0.2 or p['current_pos'] >= cfg['max'] - 0.2:
                    p['is_crossing'] = True

            # Once crossing begins, continue smoothly until reaching the opposite sidewalk
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
"""

with open(PED_PATH, 'w', encoding='utf-8') as f:
    f.write(ped_code)

print(f"Installed fluid non-stop pedestrian crossing supervisor in {PED_PATH}")
