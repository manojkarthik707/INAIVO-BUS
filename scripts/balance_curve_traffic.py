import xml.etree.ElementTree as ET
import random

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
ROU_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"

tree_net = ET.parse(NET_PATH)
root_net = tree_net.getroot()

# Build directed graph of connections
adj = {}
for conn in root_net.findall('connection'):
    f = conn.get('from')
    t = conn.get('to')
    dir_ = conn.get('dir')
    if dir_ not in ['t', 'T'] and f != f"-{t}" and t != f"-{f}":
        if f not in adj:
            adj[f] = set()
        adj[f].add(t)

# Find all closed circuits in the network (4 to 14 edges)
all_circuits = []

def find_cycles(start_edge, current_edge, path, visited):
    if len(path) > 14:
        return
    for nxt in adj.get(current_edge, []):
        if nxt == start_edge and len(path) >= 4:
            all_circuits.append(list(path))
        elif nxt not in visited and len(path) < 14:
            visited.add(nxt)
            path.append(nxt)
            find_cycles(start_edge, nxt, path, visited)
            path.pop()
            visited.remove(nxt)

for edge in list(adj.keys()):
    find_cycles(edge, edge, [edge], {edge})

print(f"Total discovered circuits: {len(all_circuits)}")

# Categorize circuits:
# 1. Main Curve Loop circuits (using edges 7, -7, 6, -6, 8, -8, 9, -9, 4, -4)
curve_circuits = [c for c in all_circuits if any(e in c for e in ['7', '-7', '6', '-6', '8', '-8', '9', '-9', '4', '-4', '0', '-0', '2', '-2', '3', '-3']) and 'shortcut_east' not in c and 'shortcut_west' not in c]

# 2. Outer Highway loop circuits (using outer_west, 13, 11, 14, 20, 16, 19, 15)
outer_circuits = [c for c in all_circuits if any(e in c for e in ['outer_west', '-outer_west', '13', '-13', '11', '-11', '14', '-14', '20', '-20', '19', '-19', '18', '-18', '21', '-21', '22', '-22']) and 'shortcut_east' not in c and 'shortcut_west' not in c]

# 3. Shortcut Parkway circuits (only 10 vehicles)
shortcut_circuits = [c for c in all_circuits if 'shortcut_east' in c or 'shortcut_west' in c]

print(f"Curve circuits: {len(curve_circuits)}")
print(f"Outer highway circuits: {len(outer_circuits)}")
print(f"Shortcut circuits: {len(shortcut_circuits)}")

rou_root = ET.Element('routes')

# Multi-modal vehicle types
proto_vtypes = [
    {'id': 'MotorbikeSimple',             'vClass': 'motorcycle', 'guiShape': 'motorcycle', 'length': '2.2', 'width': '0.9', 'minGap': '2.5', 'maxSpeed': '16.0'},
    {'id': 'ScooterSimple',               'vClass': 'moped',      'guiShape': 'motorcycle', 'length': '1.9', 'width': '0.8', 'minGap': '2.5', 'maxSpeed': '13.0'},
    {'id': 'BusSimple',                   'vClass': 'bus',        'guiShape': 'bus',        'length': '10.5','width': '2.6', 'minGap': '3.2', 'maxSpeed': '14.0'},
    {'id': 'MercedesBenzSprinterSimple',  'vClass': 'delivery',   'guiShape': 'delivery',   'length': '6.0', 'width': '2.1', 'minGap': '2.8', 'maxSpeed': '15.0'},
    {'id': 'TeslaModel3Simple',           'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.7', 'width': '1.8', 'minGap': '2.8', 'maxSpeed': '16.0'},
    {'id': 'ToyotaPriusSimple',           'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.5', 'width': '1.7', 'minGap': '2.8', 'maxSpeed': '16.0'},
    {'id': 'CitroenCZeroSimple',          'vClass': 'passenger',  'guiShape': 'passenger',  'length': '3.5', 'width': '1.5', 'minGap': '2.5', 'maxSpeed': '15.0'},
    {'id': 'BmwX5Simple',                 'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.9', 'width': '2.0', 'minGap': '2.8', 'maxSpeed': '16.0'},
]

for vt in proto_vtypes:
    ET.SubElement(rou_root, 'vType', {
        'id': vt['id'],
        'vClass': vt['vClass'],
        'guiShape': vt['guiShape'],
        'accel': '2.8',
        'decel': '4.5',
        'sigma': '0.2',
        'length': vt['length'],
        'width': vt['width'],
        'minGap': vt['minGap'],
        'maxSpeed': vt['maxSpeed'],
        'lcStrategic': '1.0',
        'lcCooperative': '1.0',
        'lcPushy': '0.0',
        'lcAssertive': '1.0',
        'tau': '0.65',
    })

# 3 Transit Buses on distinct arterial & curve routes
bus_circuits = [
    curve_circuits[0] if curve_circuits else all_circuits[0],
    outer_circuits[0] if outer_circuits else all_circuits[1],
    curve_circuits[1 % len(curve_circuits)] if curve_circuits else all_circuits[2],
]

for idx, b_circ in enumerate(bus_circuits):
    r_id = f"route_bus_{idx+1}"
    ET.SubElement(rou_root, 'route', {'id': r_id, 'edges': " ".join(b_circ)})
    ET.SubElement(rou_root, 'vehicle', {
        'id': f"transit_bus_{idx+1}",
        'type': 'BusSimple',
        'route': r_id,
        'depart': '0.00',
        'departLane': 'best',
        'departPos': 'random',
        'departSpeed': 'max',
        'reroute': 'false', # Fixed circuit: prevents diverting into shortcut!
        'color': '1.0,0.7,0.1'
    })

# 97 remaining multi-modal vehicles:
# - 50 Vehicles on the Main Curve Loop (50%)
# - 35 Vehicles on Outer Highways & Avenues (35%)
# - 12 Vehicles on Shortcut Parkway (12%)
proto_pool = (
    ['MotorbikeSimple'] * 25 +
    ['ScooterSimple'] * 20 +
    ['TeslaModel3Simple'] * 12 +
    ['ToyotaPriusSimple'] * 12 +
    ['CitroenCZeroSimple'] * 11 +
    ['BmwX5Simple'] * 10 +
    ['MercedesBenzSprinterSimple'] * 7
)

random.seed(42)
random.shuffle(proto_pool)

for idx, proto_type in enumerate(proto_pool):
    if idx < 50:
        # Main Curve Roads
        circ = curve_circuits[idx % len(curve_circuits)] if curve_circuits else all_circuits[idx % len(all_circuits)]
    elif idx < 85:
        # Outer Highways & Avenues
        circ = outer_circuits[(idx - 50) % len(outer_circuits)] if outer_circuits else all_circuits[idx % len(all_circuits)]
    else:
        # Shortcut Parkway (Only 12 vehicles!)
        circ = shortcut_circuits[(idx - 85) % len(shortcut_circuits)] if shortcut_circuits else all_circuits[idx % len(all_circuits)]

    r_id = f"route_{idx}"
    ET.SubElement(rou_root, 'route', {'id': r_id, 'edges': " ".join(circ)})

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
        'departLane': 'random',
        'departPos': 'random',
        'departSpeed': 'max',
        'reroute': 'false', # Fixed routes keep all roads populated!
        'color': col
    })

rou_tree = ET.ElementTree(rou_root)
rou_tree.write(ROU_PATH, encoding='utf-8', xml_declaration=True)
print(f"Generated 100-vehicle fleet heavily utilizing Main Curve Loop (50%), Outer Highways (35%), and Shortcut (12%) in {ROU_PATH}")
