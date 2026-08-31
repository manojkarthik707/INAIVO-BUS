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

# Find all closed circuits of length 4 to 12
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

for edge in adj.keys():
    find_cycles(edge, edge, [edge], {edge})

print(f"Total closed forward-flowing circuits discovered: {len(all_circuits)}")

# Filter circuits that use the shortcut road
shortcut_circuits = [c for c in all_circuits if 'shortcut_east' in c or 'shortcut_west' in c]
standard_circuits = [c for c in all_circuits if 'shortcut_east' not in c and 'shortcut_west' not in c]

print(f"Circuits using shortcut road: {len(shortcut_circuits)}")
print(f"Circuits on arterial roads: {len(standard_circuits)}")

# Build multimodal fleet of 60 active vehicles
# 30 vehicles on standard circuits + 30 vehicles dedicated to shortcut circuits!
fleet_circuits = []
for i in range(30):
    fleet_circuits.append(standard_circuits[i % len(standard_circuits)])
for i in range(30):
    fleet_circuits.append(shortcut_circuits[i % len(shortcut_circuits)])

# Define multi-modal vehicle type distribution
veh_types = [
    # Buses (BUS_01, BUS_02, BUS_03)
    {'type': 'bus', 'length': '10.5', 'width': '2.6', 'color': '1.0,0.7,0.1', 'maxSpeed': '14.0', 'minGap': '3.2'},
    # Passenger Cars
    {'type': 'passenger', 'length': '4.5', 'width': '1.8', 'color': '0.1,0.5,0.9', 'maxSpeed': '16.0', 'minGap': '2.8'},
    # Motorcycles / Scooters
    {'type': 'motorcycle', 'length': '2.2', 'width': '0.9', 'color': '0.9,0.2,0.1', 'maxSpeed': '15.0', 'minGap': '2.5'},
    # Scooters
    {'type': 'scooter', 'length': '1.9', 'width': '0.8', 'color': '0.2,0.8,0.3', 'maxSpeed': '12.0', 'minGap': '2.5'},
    # Bicycles
    {'type': 'bicycle', 'length': '1.7', 'width': '0.6', 'color': '0.8,0.8,0.2', 'maxSpeed': '7.0', 'minGap': '2.0'},
]

rou_root = ET.Element('routes')

# Add vType elements with zero-clipping Indian parameters
for vt in veh_types:
    ET.SubElement(rou_root, 'vType', {
        'id': vt['type'],
        'accel': '2.6',
        'decel': '4.5',
        'sigma': '0.2',
        'length': vt['length'],
        'width': vt['width'],
        'minGap': vt['minGap'],
        'maxSpeed': vt['maxSpeed'],
        'guiShape': 'bus' if vt['type'] == 'bus' else ('motorcycle' if vt['type'] in ['motorcycle', 'scooter'] else ('bicycle' if vt['type'] == 'bicycle' else 'passenger')),
        'lcStrategic': '1.0',
        'lcCooperative': '1.0',
        'lcPushy': '0.0',
        'lcAssertive': '1.0',
        'tau': '0.7',
    })

# Add 3 Dedicated Transit Buses on looping routes
bus_circuits = [
    # Bus 1 on arterial loop
    standard_circuits[0],
    # Bus 2 on shortcut loop
    shortcut_circuits[0] if shortcut_circuits else standard_circuits[1],
    # Bus 3 on reverse arterial loop
    standard_circuits[2 % len(standard_circuits)],
]

for idx, b_circ in enumerate(bus_circuits):
    r_id = f"route_bus_{idx+1}"
    ET.SubElement(rou_root, 'route', {
        'id': r_id,
        'edges': " ".join(b_circ)
    })
    ET.SubElement(rou_root, 'vehicle', {
        'id': f"BUS_0{idx+1}",
        'type': 'bus',
        'route': r_id,
        'depart': '0.00',
        'departLane': 'best',
        'departSpeed': 'max',
        'reroute': 'true',
        'color': '1.0,0.7,0.1'
    })

# Add remaining 57 vehicles (mix of cars, motorcycles, scooters, bikes)
type_pool = (
    ['passenger'] * 24 +
    ['motorcycle'] * 16 +
    ['scooter'] * 12 +
    ['bicycle'] * 5
)

random.seed(42)
random.shuffle(type_pool)

for idx, v_type in enumerate(type_pool):
    circ = fleet_circuits[idx % len(fleet_circuits)]
    r_id = f"route_{idx}"
    ET.SubElement(rou_root, 'route', {
        'id': r_id,
        'edges': " ".join(circ)
    })
    
    # Pick a vibrant color
    if v_type == 'passenger':
        colors = ['0.1,0.5,0.9', '0.85,0.15,0.15', '0.9,0.9,0.9', '0.15,0.15,0.15', '0.2,0.7,0.4', '0.95,0.65,0.1']
    elif v_type in ['motorcycle', 'scooter']:
        colors = ['0.9,0.1,0.1', '0.1,0.8,0.8', '0.9,0.8,0.1', '0.5,0.1,0.8', '0.1,0.2,0.9']
    else:
        colors = ['0.2,0.8,0.2', '0.8,0.2,0.8', '0.2,0.2,0.8']
    
    col = random.choice(colors)

    ET.SubElement(rou_root, 'vehicle', {
        'id': str(idx),
        'type': v_type,
        'route': r_id,
        'depart': f"{idx * 0.4:.2f}",
        'departLane': 'best',
        'departSpeed': 'max',
        'reroute': 'true',
        'color': col
    })

rou_tree = ET.ElementTree(rou_root)
rou_tree.write(ROU_PATH, encoding='utf-8', xml_declaration=True)
print(f"Generated 60 multi-modal vehicles actively circulating through the shortcut road in {ROU_PATH}")
