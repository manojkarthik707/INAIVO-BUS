import xml.etree.ElementTree as ET
import os

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
ROU_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"

tree = ET.parse(NET_PATH)
root = tree.getroot()

# Extract all valid non-internal edges
all_edges = set([e.get('id') for e in root.findall('edge') if not e.get('id', '').startswith(':')])

# Build forward connectivity graph (no U-turns)
connections = {}
for conn in root.findall('connection'):
    f = conn.get('from')
    t = conn.get('to')
    d = conn.get('dir')
    if f and t and not f.startswith(':') and not t.startswith(':'):
        rev = f[1:] if f.startswith('-') else ('-' + f)
        if t != rev and d != 't':
            connections.setdefault(f, set()).add(t)

# DFS to find forward closed loops
def find_forward_circuit(start_edge, min_len=6, max_len=20):
    valid = []
    def dfs(curr, path):
        if len(path) >= max_len:
            return
        for nxt in connections.get(curr, []):
            if nxt == start_edge and len(path) >= min_len:
                valid.append(path)
                return
            elif nxt not in path:
                rev = curr[1:] if curr.startswith('-') else ('-' + curr)
                if nxt != rev:
                    dfs(nxt, path + [nxt])
    dfs(start_edge, [start_edge])
    return valid[0] if valid else None

# Collect loops starting from every edge
circuits = []
for edge in sorted(list(all_edges)):
    c = find_forward_circuit(edge)
    if c:
        circuits.append(c)

print(f"Found {len(circuits)} forward loop routes across the city network.")

# Build infinite repeat loop routes
def make_infinite_loop(circuit, repeat=35):
    return " ".join(circuit * repeat)

NUM_TOTAL_VEHICLES = 90
vehicles = []

# Commercial Buses: BUS_01 (id=0), BUS_02 (id=1), BUS_03 (id=2)
# Spread cleanly on 3 distinct major circuits
bus_routes = [circuits[0], circuits[len(circuits)//3], circuits[2*len(circuits)//3]]
for i in range(3):
    depart_val = i * 0.40
    vehicles.append({
        'id': str(i),
        'type': 'bus',
        'depart': depart_val,
        'departLane': '0',
        'departSpeed': 'max',
        'route': make_infinite_loop(bus_routes[i])
    })

# Other 87 vehicles (cars + additional transit buses) distributed across all 52 circuits
for v_id in range(3, NUM_TOTAL_VEHICLES):
    c_idx = (v_id - 3) % len(circuits)
    depart_val = 1.20 + (v_id - 3) * 0.35
    v_type = "bus" if (v_id % 6 == 0) else "passenger"
    vehicles.append({
        'id': str(v_id),
        'type': v_type,
        'depart': depart_val,
        'departLane': 'random',
        'departSpeed': 'max',
        'route': make_infinite_loop(circuits[c_idx])
    })

# Ensure strictly non-decreasing departure time ordering
vehicles.sort(key=lambda x: x['depart'])

output_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>\n',
    '<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n\n',
    '    <!-- Realistic Multi-Lane Urban Vehicle Types with Sublane Overtaking & Lane Balancing -->\n',
    '    <vType id="bus" vClass="bus" carFollowModel="IDM" accel="2.2" decel="4.0" length="9.5" minGap="3.5" maxSpeed="15.0" speedFactor="1.3" speedDev="0.05" tau="1.0" laneChangeModel="SL2015" lcStrategic="1.2" lcCooperative="1.0" lcSpeedGain="1.5" lcKeepRight="0.0" lcOvertakeRight="0.5" lcSublane="1.0" />\n',
    '    <vType id="passenger" vClass="passenger" carFollowModel="IDM" accel="3.2" decel="5.0" length="4.5" minGap="2.5" maxSpeed="20.0" speedFactor="1.4" speedDev="0.1" tau="0.9" laneChangeModel="SL2015" lcStrategic="1.5" lcCooperative="1.0" lcSpeedGain="2.5" lcKeepRight="0.0" lcOvertakeRight="0.8" lcSublane="1.0" />\n\n'
]

for v in vehicles:
    output_lines.append(f'    <vehicle id="{v["id"]}" type="{v["type"]}" depart="{v["depart"]:.2f}" departLane="{v["departLane"]}" departSpeed="{v["departSpeed"]}">\n')
    output_lines.append(f'        <route edges="{v["route"]}" />\n')
    output_lines.append('    </vehicle>\n')

output_lines.append('</routes>\n')

with open(ROU_PATH, 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print(f"Generated {len(vehicles)} vehicles with sorted departure times and SL2015 multi-lane model into {ROU_PATH}")
