import xml.etree.ElementTree as ET
import random

CFG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.sumocfg"
NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
ROU_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"

# ==============================================================================
# 1. SUMOCFG: ZERO TELEPORTS, ZERO LATERAL WANDERING
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
    <waiting-time-memory value="300" />
    <lateral-resolution value="0.0" />
    <lanechange.duration value="0.5" />
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

# ==============================================================================
# 2. DISCOVER ALL VALID CONTIGUOUS LOOPS
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

random.seed(42)
random.shuffle(all_loops)

# ==============================================================================
# 3. CONFIGURE AGILE URBAN VEHICLE TYPES (NO BULKY WEDGING, NO SUB-LANE CLIPPING)
# ==============================================================================
rou_root = ET.Element('routes')

proto_vtypes = [
    # 🏍️ Motorcycles & Scooters: Agile, stay centered in lane, safe minGap
    {'id': 'MotorbikeSimple',             'vClass': 'motorcycle', 'guiShape': 'motorcycle', 'length': '2.2', 'width': '0.9', 'minGap': '3.0', 'maxSpeed': '15.0'},
    {'id': 'ScooterSimple',               'vClass': 'moped',      'guiShape': 'motorcycle', 'length': '1.9', 'width': '0.8', 'minGap': '3.0', 'maxSpeed': '13.0'},
    # 🚌 Transit Buses: Agile 6.5m urban profile so turns never get stuck across corners
    {'id': 'BusSimple',                   'vClass': 'bus',        'guiShape': 'bus',        'length': '6.8', 'width': '2.2', 'minGap': '4.0', 'maxSpeed': '14.0'},
    # 🚐 Delivery Sprinters
    {'id': 'MercedesBenzSprinterSimple',  'vClass': 'delivery',   'guiShape': 'delivery',   'length': '5.8', 'width': '2.0', 'minGap': '3.8', 'maxSpeed': '14.0'},
    # 🚗 Passenger Cars: Realistic lengths and safe following gaps
    {'id': 'TeslaModel3Simple',           'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.6', 'width': '1.8', 'minGap': '3.8', 'maxSpeed': '15.0'},
    {'id': 'ToyotaPriusSimple',           'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.4', 'width': '1.7', 'minGap': '3.8', 'maxSpeed': '15.0'},
    {'id': 'CitroenCZeroSimple',          'vClass': 'passenger',  'guiShape': 'passenger',  'length': '3.5', 'width': '1.5', 'minGap': '3.2', 'maxSpeed': '14.0'},
    {'id': 'BmwX5Simple',                 'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.8', 'width': '1.9', 'minGap': '3.8', 'maxSpeed': '15.0'},
]

for vt in proto_vtypes:
    ET.SubElement(rou_root, 'vType', {
        'id': vt['id'],
        'vClass': vt['vClass'],
        'guiShape': vt['guiShape'],
        'accel': '2.8',
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

# 70 Smooth, Perfectly Spaced Multi-Modal Vehicles
proto_pool = (
    ['MotorbikeSimple'] * 18 +
    ['ScooterSimple'] * 14 +
    ['TeslaModel3Simple'] * 9 +
    ['ToyotaPriusSimple'] * 9 +
    ['CitroenCZeroSimple'] * 8 +
    ['BmwX5Simple'] * 7 +
    ['MercedesBenzSprinterSimple'] * 5
)

random.shuffle(proto_pool)

for idx, proto_type in enumerate(proto_pool):
    loop = all_loops[(idx + 4) % len(all_loops)]
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
print(f"Generated 73-vehicle fluid fleet in {ROU_PATH}")
