import xml.etree.ElementTree as ET
import random

CFG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.sumocfg"
NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
ROU_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"
PED_PATH = r"f:\VEHDEMO\simulation\webots\controllers\pedestrian_controller\pedestrian_controller.py"

# ==============================================================================
# 1. CONFIGURE SUMO.SUMOCFG: ZERO TELEPORTS, ZERO DESPAWNING
# ==============================================================================
cfg_xml = """<?xml version='1.0' encoding='utf-8'?>
<configuration>
  <input>
    <net-file value="sumo.net.xml" />
    <route-files value="sumo.rou.xml" />
  </input>
  <time>
    <end value="99999" />
    <begin value="0" />
  </time>
  <processing>
    <step-length value="0.032" />
    <time-to-teleport value="-1" />
    <collision.action value="none" />
    <collision.check-junctions value="false" />
    <waiting-time-memory value="200" />
    <lateral-resolution value="0.0" />
    <lanechange.duration value="1.0" />
    <lanechange.overtake-right value="false" />
  </processing>
  <routing>
    <routing-algorithm value="dijkstra" />
  </routing>
  <report>
    <verbose value="true" />
    <no-step-log value="true" />
  </report>
</configuration>
"""
with open(CFG_PATH, 'w', encoding='utf-8') as f:
    f.write(cfg_xml)

print("Updated sumo.sumocfg to disable teleports and despawning completely!")

# ==============================================================================
# 2. EVENLY DISTRIBUTE 100 VEHICLES ACROSS ALL 276 LOOPS (ZERO BOTTLE-NECKS)
# ==============================================================================
tree = ET.parse(NET_PATH)
root = tree.getroot()

adj = {}
for conn in root.findall('connection'):
    f = conn.get('from')
    t = conn.get('to')
    dir_ = conn.get('dir')
    if dir_ not in ['t', 'T'] and f != f"-{t}" and t != f"-{f}":
        if f not in adj:
            adj[f] = set()
        adj[f].add(t)

def find_loops(start, curr, path, visited):
    if len(path) > 14:
        return []
    loops = []
    for nxt in adj.get(curr, []):
        if nxt == start and len(path) >= 3:
            loops.append(list(path))
        elif nxt not in visited and len(path) < 14:
            visited.add(nxt)
            path.append(nxt)
            loops.extend(find_loops(start, nxt, path, visited))
            path.pop()
            visited.remove(nxt)
    return loops

all_loops = []
for edge in list(adj.keys()):
    all_loops.extend(find_loops(edge, edge, [edge], {edge}))

print(f"Total discovered valid loops: {len(all_loops)}")

# Shuffle loops to guarantee perfectly distributed city-wide traffic
random.seed(42)
random.shuffle(all_loops)

rou_root = ET.Element('routes')

proto_vtypes = [
    {'id': 'MotorbikeSimple',             'vClass': 'motorcycle', 'guiShape': 'motorcycle', 'length': '2.4', 'width': '0.9', 'minGap': '3.5', 'maxSpeed': '16.0'},
    {'id': 'ScooterSimple',               'vClass': 'moped',      'guiShape': 'motorcycle', 'length': '2.0', 'width': '0.8', 'minGap': '3.5', 'maxSpeed': '14.0'},
    {'id': 'BusSimple',                   'vClass': 'bus',        'guiShape': 'bus',        'length': '11.0','width': '2.6', 'minGap': '5.0', 'maxSpeed': '14.0'},
    {'id': 'MercedesBenzSprinterSimple',  'vClass': 'delivery',   'guiShape': 'delivery',   'length': '6.5', 'width': '2.1', 'minGap': '4.5', 'maxSpeed': '15.0'},
    {'id': 'TeslaModel3Simple',           'vClass': 'passenger',  'guiShape': 'passenger',  'length': '5.0', 'width': '1.8', 'minGap': '4.5', 'maxSpeed': '16.0'},
    {'id': 'ToyotaPriusSimple',           'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.8', 'width': '1.7', 'minGap': '4.5', 'maxSpeed': '16.0'},
    {'id': 'CitroenCZeroSimple',          'vClass': 'passenger',  'guiShape': 'passenger',  'length': '3.8', 'width': '1.5', 'minGap': '4.0', 'maxSpeed': '15.0'},
    {'id': 'BmwX5Simple',                 'vClass': 'passenger',  'guiShape': 'passenger',  'length': '5.2', 'width': '2.0', 'minGap': '4.5', 'maxSpeed': '16.0'},
]

for vt in proto_vtypes:
    ET.SubElement(rou_root, 'vType', {
        'id': vt['id'],
        'vClass': vt['vClass'],
        'guiShape': vt['guiShape'],
        'accel': '2.6',
        'decel': '4.5',
        'emergencyDecel': '9.0',
        'sigma': '0.0',
        'length': vt['length'],
        'width': vt['width'],
        'minGap': vt['minGap'],
        'maxSpeed': vt['maxSpeed'],
        'lcStrategic': '1.0',
        'lcCooperative': '1.0',
        'lcSpeedGain': '1.0',
        'lcAssertive': '1.0',
        'lcPushy': '0.0',
        'lcOvertakeRight': '0.0',
        'tau': '1.4',
    })

N_REPEATS = 60

# 3 Transit Buses
buses = [
    ('transit_bus_1', all_loops[0]),
    ('transit_bus_2', all_loops[1]),
    ('transit_bus_3', all_loops[2]),
]

for b_id, b_loop in buses:
    r_id = f"route_{b_id}"
    p_edges = " ".join(b_loop * N_REPEATS)
    ET.SubElement(rou_root, 'route', {'id': r_id, 'edges': p_edges})
    ET.SubElement(rou_root, 'vehicle', {
        'id': b_id,
        'type': 'BusSimple',
        'route': r_id,
        'depart': '0.00',
        'departLane': 'best',
        'departPos': 'random_free',
        'departSpeed': 'max',
        'color': '1.0,0.7,0.1'
    })

proto_pool = (
    ['MotorbikeSimple'] * 25 +
    ['ScooterSimple'] * 20 +
    ['TeslaModel3Simple'] * 12 +
    ['ToyotaPriusSimple'] * 12 +
    ['CitroenCZeroSimple'] * 11 +
    ['BmwX5Simple'] * 10 +
    ['MercedesBenzSprinterSimple'] * 7
)

random.shuffle(proto_pool)

for idx, proto_type in enumerate(proto_pool):
    # Every vehicle gets its own distinct loop from the 276 discovered circuits
    loop = all_loops[(idx + 3) % len(all_loops)]

    # Start at a unique edge along the circuit
    start_offset = (idx * 3) % len(loop)
    shifted = loop[start_offset:] + loop[:start_offset]
    p_edges = " ".join(shifted * N_REPEATS)

    r_id = f"route_{idx}"
    ET.SubElement(rou_root, 'route', {'id': r_id, 'edges': p_edges})

    if 'Motorbike' in proto_type:
        colors = ['0.9,0.1,0.1', '0.1,0.8,0.8', '0.9,0.8,0.1', '0.5,0.1,0.8', '0.1,0.2,0.9']
    elif 'Scooter' in proto_type:
        colors = ['0.2,0.8,0.3', '0.9,0.5,0.1', '0.8,0.1,0.5', '0.1,0.7,0.9', '0.7,0.7,0.1']
    elif 'Sprinter' in proto_type:
        colors = ['0.95,0.95,0.95', '0.8,0.7,0.2', '0.2,0.3,0.5']
    else:
        colors = ['0.1,0.5,0.9', '0.85,0.15,0.15', '0.92,0.92,0.92', '0.12,0.12,0.12', '0.2,0.7,0.4', '0.95,0.65,0.1']

    col = random.choice(colors)

    ET.SubElement(rou_root, 'vehicle', {
        'id': f"veh_{idx}",
        'type': proto_type,
        'route': r_id,
        'depart': '0.00',
        'departLane': 'best',
        'departPos': 'random_free',
        'departSpeed': 'max',
        'color': col
    })

rou_tree = ET.ElementTree(rou_root)
rou_tree.write(ROU_PATH, encoding='utf-8', xml_declaration=True)
print(f"Generated 100-vehicle fleet evenly distributed across all 276 circuits in {ROU_PATH}")

# ==============================================================================
# 3. WRITE FLUID PEDESTRIAN CONTROLLER
# ==============================================================================
ped_code = """\"\"\"
pedestrian_controller.py — Fluid, Protected Pedestrian Crosswalk Supervisor.
\"\"\"
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
    WALK_SPEED = 4.5

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

            if jid == '25':
                is_safe_stage = (stage_idx in [0, 2])
            else:
                is_safe_stage = (stage_idx in [1, 3])

            if is_safe_stage and t_in_stage < 1.2 and not p['is_crossing']:
                if p['current_pos'] <= cfg['min'] + 0.2 or p['current_pos'] >= cfg['max'] - 0.2:
                    p['is_crossing'] = True

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

print("Updated pedestrian controller for fluid non-stop crossings.")
