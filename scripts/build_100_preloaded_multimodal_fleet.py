import xml.etree.ElementTree as ET
import random

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
ROU_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"

tree = ET.parse(NET_PATH)
root = tree.getroot()

# Build adjacency map of edges
adj = {}
for conn in root.findall('connection'):
    f = conn.get('from')
    t = conn.get('to')
    dir_ = conn.get('dir')
    if dir_ != 'T': # Disallow U-turns
        if f not in adj:
            adj[f] = set()
        adj[f].add(t)

# Find closed forward-flowing circuits
all_circuits = []

def find_cycles(start_edge, current_edge, path, visited):
    if len(path) > 12:
        return
    for nxt in adj.get(current_edge, []):
        if nxt == start_edge and len(path) >= 4:
            all_circuits.append(list(path))
        elif nxt not in visited and len(path) < 12:
            visited.add(nxt)
            path.append(nxt)
            find_cycles(start_edge, nxt, path, visited)
            path.pop()
            visited.remove(nxt)

for edge in list(adj.keys()):
    find_cycles(edge, edge, [edge], {edge})

shortcut_circuits = [c for c in all_circuits if 'shortcut_east' in c or 'shortcut_west' in c]
standard_circuits = [c for c in all_circuits if 'shortcut_east' not in c and 'shortcut_west' not in c]

# Get all unique network edges to assign distinct start positions
all_network_edges = list(set([e.get('id') for e in root.findall('edge') if not e.get('id', '').startswith(':')]))

rou_root = ET.Element('routes')

# 1. Define explicit Webots-compatible vehicle types
vtypes = [
    {'id': 'bus',         'guiShape': 'bus',        'length': '10.5', 'width': '2.6', 'minGap': '3.2', 'maxSpeed': '14.0'},
    {'id': 'passenger',   'guiShape': 'passenger',  'length': '4.5',  'width': '1.8', 'minGap': '2.8', 'maxSpeed': '16.0'},
    {'id': 'motorcycle',  'guiShape': 'motorcycle', 'length': '2.2',  'width': '0.9', 'minGap': '2.5', 'maxSpeed': '15.0'},
    {'id': 'scooter',     'guiShape': 'motorcycle', 'length': '1.9',  'width': '0.8', 'minGap': '2.5', 'maxSpeed': '12.0'},
    {'id': 'delivery',    'guiShape': 'delivery',   'length': '6.0',  'width': '2.1', 'minGap': '2.8', 'maxSpeed': '15.0'},
]

for vt in vtypes:
    ET.SubElement(rou_root, 'vType', {
        'id': vt['id'],
        'accel': '2.8',
        'decel': '4.5',
        'sigma': '0.2',
        'length': vt['length'],
        'width': vt['width'],
        'minGap': vt['minGap'],
        'maxSpeed': vt['maxSpeed'],
        'guiShape': vt['guiShape'],
        'lcStrategic': '1.0',
        'lcCooperative': '1.0',
        'lcPushy': '0.0',
        'lcAssertive': '1.0',
        'tau': '0.65',
    })

# 2. Add 3 Dedicated Transit Buses
bus_routes = [
    standard_circuits[0],
    shortcut_circuits[0],
    standard_circuits[1 % len(standard_circuits)],
]

for idx, b_circ in enumerate(bus_routes):
    r_id = f"route_bus_{idx+1}"
    ET.SubElement(rou_root, 'route', {'id': r_id, 'edges': " ".join(b_circ)})
    ET.SubElement(rou_root, 'vehicle', {
        'id': f"BUS_0{idx+1}",
        'type': 'bus',
        'route': r_id,
        'depart': '0.00',
        'departLane': 'best',
        'departPos': 'random',
        'departSpeed': 'max',
        'reroute': 'true',
        'color': '1.0,0.7,0.1'
    })

# 3. Add 97 remaining multi-modal vehicles:
# 25 Motorcycles + 20 Scooters + 45 Passenger Cars + 7 Delivery Vans = 97 vehicles
fleet_composition = (
    ['motorcycle'] * 25 +
    ['scooter'] * 20 +
    ['passenger'] * 45 +
    ['delivery'] * 7
)

random.seed(42)
random.shuffle(fleet_composition)

# Map available circuits indexed by starting edge to maximize immediate insertion
circuits_by_start = {}
for c in shortcut_circuits + standard_circuits:
    s = c[0]
    if s not in circuits_by_start:
        circuits_by_start[s] = []
    circuits_by_start[s].append(c)

start_edge_list = list(circuits_by_start.keys())

for idx, v_type in enumerate(fleet_composition):
    start_edge = start_edge_list[idx % len(start_edge_list)]
    avail = circuits_by_start[start_edge]
    circ = avail[idx % len(avail)]

    r_id = f"route_{idx}"
    ET.SubElement(rou_root, 'route', {'id': r_id, 'edges': " ".join(circ)})

    if v_type == 'motorcycle':
        colors = ['0.9,0.1,0.1', '0.1,0.8,0.8', '0.9,0.8,0.1', '0.5,0.1,0.8', '0.1,0.2,0.9']
    elif v_type == 'scooter':
        colors = ['0.2,0.8,0.3', '0.9,0.5,0.1', '0.8,0.1,0.5', '0.1,0.7,0.9', '0.7,0.7,0.1']
    elif v_type == 'delivery':
        colors = ['0.95,0.95,0.95', '0.8,0.7,0.2', '0.2,0.3,0.5']
    else:
        colors = ['0.1,0.5,0.9', '0.85,0.15,0.15', '0.92,0.92,0.92', '0.12,0.12,0.12', '0.2,0.7,0.4', '0.95,0.65,0.1']

    col = random.choice(colors)

    # PRELOAD ALL 100 VEHICLES IMMEDIATELY
    ET.SubElement(rou_root, 'vehicle', {
        'id': str(idx),
        'type': v_type,
        'route': r_id,
        'depart': '0.00',
        'departLane': 'random',
        'departPos': 'random',
        'departSpeed': 'max',
        'reroute': 'true',
        'color': col
    })

rou_tree = ET.ElementTree(rou_root)
rou_tree.write(ROU_PATH, encoding='utf-8', xml_declaration=True)
print(f"Generated 100-vehicle preloaded fleet with instant multi-edge insertion in {ROU_PATH}")
