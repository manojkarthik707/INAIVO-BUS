"""
pedestrian_controller.py — Fully Synchronized Directional Pedestrian Crosswalks.

Exact Per-Crosswalk Phase Rules:
A pedestrian crosswalk is SAFE to cross ONLY when the vehicular approach crossing that zebra line is on RED.

Junction 25 Signal Stages:
  Stage 0 (0-7s):   EAST Green   -> PED_J25_EAST is RED.  (SOUTH, NORTH, WEST are SAFE!)
  Stage 1 (7-14s):  NORTH Green  -> PED_J25_NORTH is RED. (SOUTH, EAST, WEST are SAFE!)
  Stage 2 (14-21s): WEST Green   -> PED_J25_WEST is RED.  (SOUTH, NORTH, EAST are SAFE!)
  Stage 3 (21-28s): SOUTH Green  -> PED_J25_SOUTH is RED. (NORTH, EAST, WEST are SAFE!)

Junctions 26 & 27 Signal Stages:
  Stage 0 (0-7s):   SOUTH Green  -> PED_J*_SOUTH is RED.  (NORTH, EAST, WEST are SAFE!)
  Stage 1 (7-14s):  EAST Green   -> PED_J*_EAST is RED.   (SOUTH, NORTH, WEST are SAFE!)
  Stage 2 (14-21s): NORTH Green  -> PED_J*_NORTH is RED.  (SOUTH, EAST, WEST are SAFE!)
  Stage 3 (21-28s): WEST Green   -> PED_J*_WEST is RED.   (SOUTH, NORTH, EAST are SAFE!)
"""

from controller import Supervisor

def main():
    robot = Supervisor()
    timestep = int(robot.getBasicTimeStep())
    if timestep <= 0:
        timestep = 32

    ped_configs = [
        # Junction 26 (-45.0, 45.0)
        {'name': 'PED_J26_SOUTH', 'jid': '26', 'approach': 'SOUTH', 'axis': 'X', 'min': -55.0, 'max': -35.0, 'fixed': 33.5},
        {'name': 'PED_J26_NORTH', 'jid': '26', 'approach': 'NORTH', 'axis': 'X', 'min': -55.0, 'max': -35.0, 'fixed': 56.5},
        {'name': 'PED_J26_EAST',  'jid': '26', 'approach': 'EAST',  'axis': 'Y', 'min': 35.0,  'max': 55.0,  'fixed': -33.5},
        {'name': 'PED_J26_WEST',  'jid': '26', 'approach': 'WEST',  'axis': 'Y', 'min': 35.0,  'max': 55.0,  'fixed': -56.5},

        # Junction 25 (45.0, -45.0)
        {'name': 'PED_J25_SOUTH', 'jid': '25', 'approach': 'SOUTH', 'axis': 'X', 'min': 35.0,  'max': 55.0,  'fixed': -56.5},
        {'name': 'PED_J25_NORTH', 'jid': '25', 'approach': 'NORTH', 'axis': 'X', 'min': 35.0,  'max': 55.0,  'fixed': -33.5},
        {'name': 'PED_J25_EAST',  'jid': '25', 'approach': 'EAST',  'axis': 'Y', 'min': -55.0, 'max': -35.0, 'fixed': 56.5},
        {'name': 'PED_J25_WEST',  'jid': '25', 'approach': 'WEST',  'axis': 'Y', 'min': -55.0, 'max': -35.0, 'fixed': 33.5},

        # Junction 27 (105.0, 93.0)
        {'name': 'PED_J27_SOUTH', 'jid': '27', 'approach': 'SOUTH', 'axis': 'X', 'min': 95.0,  'max': 115.0, 'fixed': 81.5},
        {'name': 'PED_J27_NORTH', 'jid': '27', 'approach': 'NORTH', 'axis': 'X', 'min': 95.0,  'max': 115.0, 'fixed': 104.5},
        {'name': 'PED_J27_EAST',  'jid': '27', 'approach': 'EAST',  'axis': 'Y', 'min': 83.0,  'max': 103.0, 'fixed': 116.5},
        {'name': 'PED_J27_WEST',  'jid': '27', 'approach': 'WEST',  'axis': 'Y', 'min': 83.0,  'max': 103.0, 'fixed': 93.5},
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

    print(f"Synchronized Directional Pedestrian Supervisor: {len(peds)} crosswalks online.")

    TOTAL_CYCLE = 28.0
    STAGE_LEN = 7.0
    WALK_SPEED = 4.5 # 4.5 m/s -> crosses in 3.8s, finishing cleanly within the 7.0s protected red stage

    while robot.step(timestep) != -1:
        sim_time = robot.getTime()
        dt = timestep / 1000.0
        cycle_t = sim_time % TOTAL_CYCLE
        stage_idx = int(cycle_t // STAGE_LEN)
        t_in_stage = cycle_t % STAGE_LEN

        for p in peds:
            cfg = p['cfg']
            jid = cfg['jid']
            approach = cfg['approach']

            # Determine if this specific approach currently has GREEN vehicular traffic
            if jid == '25':
                # J25: 0=EAST, 1=NORTH, 2=WEST, 3=SOUTH
                green_approach = ['EAST', 'NORTH', 'WEST', 'SOUTH'][stage_idx]
            else:
                # J26 & J27: 0=SOUTH, 1=EAST, 2=NORTH, 3=WEST
                green_approach = ['SOUTH', 'EAST', 'NORTH', 'WEST'][stage_idx]

            # Crosswalk is strictly FORBIDDEN when its approach has Green
            # Crosswalk is SAFE when its approach has RED
            is_approach_red = (approach != green_approach)

            # Initiate crossing only when vehicular traffic on this approach is SOLID RED
            # and within the first 1.0s of the red stage so pedestrian clears in 3.8s
            if is_approach_red and t_in_stage < 1.0 and not p['is_crossing']:
                if p['current_pos'] <= cfg['min'] + 0.2 or p['current_pos'] >= cfg['max'] - 0.2:
                    p['is_crossing'] = True

            # Fluid, smooth continuous crossing until reaching the sidewalk curb
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
