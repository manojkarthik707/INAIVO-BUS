"""
Add NUMBER_PLATE_SUPERVISOR Robot node to sih_mvp_traffic.wbt
and regenerate sumo.rou.xml with anti-deadlock balanced routes.
"""

import xml.etree.ElementTree as ET
import subprocess, math, random

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"
NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
ROU_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"

# ==================== 1. ADD NUMBER_PLATE_SUPERVISOR TO WBT ====================
with open(WBT_PATH, 'r', encoding='utf-8') as f:
    wbt_text = f.read()

plate_node = '''DEF NUMBER_PLATE_SUPERVISOR Robot {
  name "number_plate_supervisor"
  controller "number_plate_controller"
  supervisor TRUE
  locked TRUE
}'''

if 'number_plate_supervisor' not in wbt_text:
    # Insert before last closing } 
    idx = wbt_text.rfind('\nDEF POTHOLE_SUPERVISOR')
    if idx > 0:
        wbt_text = wbt_text[:idx] + '\n' + plate_node + wbt_text[idx:]
    else:
        wbt_text = wbt_text.rstrip().rstrip('}').rstrip() + '\n' + plate_node + '\n'
    with open(WBT_PATH, 'w', encoding='utf-8') as f:
        f.write(wbt_text)
    print("Added NUMBER_PLATE_SUPERVISOR to sih_mvp_traffic.wbt")
else:
    print("NUMBER_PLATE_SUPERVISOR already present in wbt.")

# ==================== 2. REGENERATE ANTI-DEADLOCK ROUTES ====================
tree = ET.parse(NET_PATH)
root = tree.getroot()

# Collect all valid non-internal edges
edges_by_id = {}
for edge in root.findall('edge'):
    e_id = edge.get('id')
    if e_id and not e_id.startswith(':'):
        edges_by_id[e_id] = edge

# Build adjacency list from connections
adj = {}  # from_edge -> list of to_edges
for conn in root.findall('connection'):
    f_e = conn.get('from')
    t_e = conn.get('to')
    if f_e and t_e and not f_e.startswith(':') and not t_e.startswith(':'):
        adj.setdefault(f_e, set()).add(t_e)

def find_route(start, max_hops=8):
    """Find a valid loop route starting from start edge."""
    visited = [start]
    cur = start
    for _ in range(max_hops):
        nexts = list(adj.get(cur, []))
        if not nexts:
            break
        # Prefer edges not yet visited
        unvisited = [e for e in nexts if e not in visited]
        if unvisited:
            nxt = random.choice(unvisited)
        else:
            nxt = random.choice(nexts)
        visited.append(nxt)
        cur = nxt
        if len(visited) >= 4 and nxt in list(adj.get(nxt, [])):
            break
    return visited

# Build routes per vehicle type
random.seed(42)
edge_list = [e for e in edges_by_id if not e.startswith('-')]

# Generate 300 unique routes 
all_routes = []
seen_routes = set()
attempts = 0
while len(all_routes) < 300 and attempts < 5000:
    attempts += 1
    start = random.choice(edge_list)
    r = find_route(start)
    if len(r) >= 3:
        key = tuple(r[:4])
        if key not in seen_routes:
            seen_routes.add(key)
            all_routes.append(r)

print(f"Generated {len(all_routes)} unique anti-deadlock routes")

# Vehicle type definitions
VEHICLE_TYPES = [
    # (vtype_id, accel, decel, sigma, max_speed, length, vehicle_class, count)
    ("motorbike",  2.5, 4.5, 0.4, 18.0, 2.0,  "motorcycle", 25),
    ("scooter",    2.0, 4.0, 0.5, 15.0, 1.8,  "motorcycle", 20),
    ("car",        2.0, 4.5, 0.5, 15.0, 5.0,  "passenger",  45),
    ("bus",        1.2, 3.0, 0.3, 10.0, 12.0, "bus",         3),
    ("van",        1.8, 4.0, 0.5, 12.0, 6.0,  "passenger",   7),
]

rng = random.Random(42)
rou = ET.Element('routes')

# Add vehicle types
for vtype_id, acc, dec, sig, spd, lng, vclass, _ in VEHICLE_TYPES:
    ET.SubElement(rou, 'vType', {
        'id': vtype_id,
        'accel': str(acc),
        'decel': str(dec),
        'sigma': str(sig),
        'maxSpeed': str(spd),
        'length': str(lng),
        'vClass': vclass,
        'carFollowModel': 'IDM',
        'tau': '1.5',
        'lcStrategic': '1.0',
        'lcCooperative': '0.8',
    })

route_idx = 0
vehicle_idx = 0

for vtype_id, _, _, _, _, _, _, count in VEHICLE_TYPES:
    for _ in range(count):
        r = all_routes[route_idx % len(all_routes)]
        route_idx += 1

        route_id = f"route_{vehicle_idx}"
        edges_str = " ".join(r)
        ET.SubElement(rou, 'route', {'id': route_id, 'edges': edges_str})

        veh_id = f"{'transit_bus' if vtype_id == 'bus' else vtype_id}_{vehicle_idx}"
        ET.SubElement(rou, 'vehicle', {
            'id': veh_id,
            'type': vtype_id,
            'route': route_id,
            'depart': '0.00',
            'departPos': 'random_free',
            'departLane': 'best',
            'departSpeed': 'random',
        })
        vehicle_idx += 1

# Add flow for continuous traffic to prevent deadlock
for i, edge in enumerate(edge_list[:20]):
    ET.SubElement(rou, 'flow', {
        'id': f'flow_{i}',
        'type': 'car',
        'from': edge,
        'to': rng.choice(edge_list),
        'begin': '30',
        'end': '3600',
        'period': '15',
        'departPos': 'free',
        'departSpeed': 'random',
    })

tree_rou = ET.ElementTree(rou)
ET.indent(tree_rou, space='  ')
tree_rou.write(ROU_PATH, encoding='utf-8', xml_declaration=True)
print(f"Written anti-deadlock sumo.rou.xml with {vehicle_idx} vehicles + 20 flows")

# ==================== 3. VERIFY SUMO ====================
result = subprocess.run(
    [r"C:\Program Files (x86)\Eclipse\Sumo\bin\sumo.exe",
     "-c", r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.sumocfg",
     "--step-length", "0.032", "-e", "60"],
    capture_output=True, text=True
)
print(result.stdout[-1000:])
if result.returncode == 0:
    print("SUMO validation PASSED.")
else:
    print("SUMO errors:", result.stderr[-500:])
