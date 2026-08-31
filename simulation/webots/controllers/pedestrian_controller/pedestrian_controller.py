"""
pedestrian_controller.py — Signal-Obedient Pedestrians with Precise Directional Forward Collision AEB.

AEB (Autonomous Emergency Braking) Rules:
1. Continuous Decisive Crossing: Pedestrians cross decisively at 2.8 m/s during Red phases.
2. True Directional Collision Course Detection:
   - Computes exact vehicle instantaneous velocity vector (direction of travel).
   - Only brakes if the pedestrian is directly in the vehicle's forward path corridor:
     * Longitudinal Distance Ahead: 0.4m <= d_lon <= 3.2m
     * Lateral Path Offset: d_lat <= 1.3m (directly in front of the vehicle bumper)
   - If pedestrian is in another lane, to the side, or behind the vehicle, the car DOES NOT STOP.
"""

import math
from controller import Supervisor

def main():
    robot = Supervisor()
    timestep = int(robot.getBasicTimeStep())
    if timestep <= 0:
        timestep = 32

    # Configuration for all 12 crossing pedestrians:
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
                    'current_pos': cfg['min'],
                    'target_side': 'max',
                    'is_crossing': False,
                })

    # Cache vehicle nodes
    tracked_vehicles = {}
    for i in range(80):
        v = robot.getFromDef(f"SUMO_VEHICLE{i}")
        if v:
            tf = v.getField("translation")
            if tf:
                tracked_vehicles[i] = {
                    'node': v,
                    't_field': tf,
                    'held_pos': None,
                    'last_pos': None,
                    'heading': (1.0, 0.0)
                }

    print(f"AEB Pedestrian Supervisor online: {len(peds)} pedestrians, directional forward AEB on {len(tracked_vehicles)} vehicles.")

    TOTAL_CYCLE = 28.0
    STAGE_LEN = 7.0
    WALK_SPEED = 2.8 # 2.8 m/s (~10 km/h)

    scan_counter = 0

    while robot.step(timestep) != -1:
        sim_time = robot.getTime()
        dt = timestep / 1000.0
        cycle_t = sim_time % TOTAL_CYCLE
        stage_idx = int(cycle_t // STAGE_LEN)

        # Refresh tracked vehicles periodically
        scan_counter += 1
        if scan_counter % 30 == 0:
            for i in range(80):
                if i not in tracked_vehicles:
                    v = robot.getFromDef(f"SUMO_VEHICLE{i}")
                    if v:
                        tf = v.getField("translation")
                        if tf:
                            tracked_vehicles[i] = {
                                'node': v,
                                't_field': tf,
                                'held_pos': None,
                                'last_pos': None,
                                'heading': (1.0, 0.0)
                            }

        # 1. Update Pedestrian Positions
        active_crossing_coords = []

        for p in peds:
            cfg = p['cfg']
            jid = cfg['jid']

            if jid == '25':
                active_veh_dir = ['EAST', 'NORTH', 'WEST', 'SOUTH'][stage_idx]
            else:
                active_veh_dir = ['SOUTH', 'EAST', 'NORTH', 'WEST'][stage_idx]

            cars_stopped_red = (active_veh_dir != cfg['dir'])

            if p['is_crossing'] or cars_stopped_red:
                p['is_crossing'] = True

                if p['target_side'] == 'max':
                    p['current_pos'] += WALK_SPEED * dt
                    if cfg['axis'] == 'X':
                        p['r_field'].setSFRotation([0, 0, 1, 0.0])
                    else:
                        p['r_field'].setSFRotation([0, 0, 1, 1.5708])

                    if p['current_pos'] >= cfg['max']:
                        p['current_pos'] = cfg['max']
                        p['target_side'] = 'min'
                        p['is_crossing'] = False
                        if cfg['axis'] == 'X':
                            p['r_field'].setSFRotation([0, 0, 1, 3.14159])
                        else:
                            p['r_field'].setSFRotation([0, 0, 1, -1.5708])
                else:
                    p['current_pos'] -= WALK_SPEED * dt
                    if cfg['axis'] == 'X':
                        p['r_field'].setSFRotation([0, 0, 1, 3.14159])
                    else:
                        p['r_field'].setSFRotation([0, 0, 1, -1.5708])

                    if p['current_pos'] <= cfg['min']:
                        p['current_pos'] = cfg['min']
                        p['target_side'] = 'max'
                        p['is_crossing'] = False
                        if cfg['axis'] == 'X':
                            p['r_field'].setSFRotation([0, 0, 1, 0.0])
                        else:
                            p['r_field'].setSFRotation([0, 0, 1, 1.5708])
            else:
                # Waiting on curb
                if p['current_pos'] <= cfg['min']:
                    if cfg['axis'] == 'X':
                        p['r_field'].setSFRotation([0, 0, 1, 0.0])
                    else:
                        p['r_field'].setSFRotation([0, 0, 1, 1.5708])
                else:
                    if cfg['axis'] == 'X':
                        p['r_field'].setSFRotation([0, 0, 1, 3.14159])
                    else:
                        p['r_field'].setSFRotation([0, 0, 1, -1.5708])

            if cfg['axis'] == 'X':
                curr_x = p['current_pos']
                curr_y = cfg['fixed']
            else:
                curr_x = cfg['fixed']
                curr_y = p['current_pos']

            p['t_field'].setSFVec3f([curr_x, curr_y, 1.27])

            # Track active pedestrian if in roadway
            if (p['current_pos'] > cfg['min'] + 1.2) and (p['current_pos'] < cfg['max'] - 1.2):
                active_crossing_coords.append((curr_x, curr_y))

        # 2. Forward Collision AEB Calculation
        for v_id, v_data in list(tracked_vehicles.items()):
            tf = v_data['t_field']
            try:
                v_pos = tf.getSFVec3f()
            except Exception:
                continue

            if not v_pos or abs(v_pos[0]) > 500:
                continue

            # Update heading direction of travel
            last = v_data['last_pos']
            if last is not None and v_data['held_pos'] is None:
                dx = v_pos[0] - last[0]
                dy = v_pos[1] - last[1]
                speed = math.hypot(dx, dy)
                if speed > 0.02:
                    v_data['heading'] = (dx / speed, dy / speed)

            v_data['last_pos'] = list(v_pos)
            hx, hy = v_data['heading']

            # Check if ANY pedestrian is directly in this vehicle's path corridor
            direct_collision_imminent = False
            for px, py in active_crossing_coords:
                # Relative vector from vehicle front to pedestrian
                rel_x = px - v_pos[0]
                rel_y = py - v_pos[1]

                # Longitudinal distance along vehicle travel heading
                d_lon = rel_x * hx + rel_y * hy
                # Lateral distance perpendicular to travel heading
                d_lat = abs(rel_x * (-hy) + rel_y * hx)

                # ONLY STOP IF PEDESTRIAN IS DIRECTLY IN FRONT OF THE VEHICLE'S BUMPER (Within 3.2m ahead and 1.3m lane width)
                if (0.3 <= d_lon <= 3.2) and (d_lat <= 1.35):
                    direct_collision_imminent = True
                    break

            if direct_collision_imminent:
                if v_data['held_pos'] is None:
                    v_data['held_pos'] = list(v_pos)
                else:
                    tf.setSFVec3f(v_data['held_pos'])
            else:
                v_data['held_pos'] = None

if __name__ == '__main__':
    main()
